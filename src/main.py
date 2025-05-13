import argparse
import json
import logging
import os
from datetime import datetime, timedelta

import requests
from client import AimHarderClient
from exceptions import (
    NoBookingGoal,
    BoxClosed,
    MESSAGE_BOX_IS_CLOSED,
    MESSAGE_ALREADY_BOOKED_FOR_TIME,
)
from exceptions import BookingFailed

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# Function to send telegram message
def send_telegram_message(text):
    telegram_token = os.environ["AH_TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = os.environ["AH_CHAT_ID"]
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": text
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to send telegram message: {e}")


def get_booking_goal_time(day: datetime, booking_goals):
    """Get the booking goal that satisfies the given day of the week"""
    try:
        return (
            booking_goals[str(day.weekday())]["time"],
            booking_goals[str(day.weekday())]["name"],
        )
    except KeyError:  # did not find a matching booking goal
        raise NoBookingGoal(
            f"There is no booking-goal for {day.strftime('%A, %Y-%m-%d')}."
        )


def get_class_to_book(classes: list[dict], target_time: str, class_name: str):
    if not classes or len(classes) == 0:
        raise BoxClosed(MESSAGE_BOX_IS_CLOSED)

    classes = list(filter(lambda _class: target_time in _class["timeid"], classes))
    _class = list(filter(lambda _class: class_name in _class["className"], classes))
    if len(_class) == 0:
        raise NoBookingGoal(
            f"No class with the text `{class_name}` in its name at time `{target_time}`"
        )
    return _class[0]


def main(
    email, password, booking_goals, box_name, box_id, days_in_advance, family_id=None
):
    target_day = datetime.today() + timedelta(days=days_in_advance)
    try:
        target_time, target_name = get_booking_goal_time(target_day, booking_goals)
    except NoBookingGoal as e:
        logger.info(str(e))
        send_telegram_message(f"⚠️ {str(e)}")
        return
    client = AimHarderClient(
        email=email, password=password, box_id=box_id, box_name=box_name
    )
    classes = client.get_classes(target_day, family_id)
    try:
        _class = get_class_to_book(classes, target_time, target_name)
    except (BoxClosed, NoBookingGoal) as e:
        logger.info(str(e))
        send_telegram_message(f"⚠️ {str(e)}")
        return

    if _class["bookState"] == 1:
        logger.info("Class already booked. Nothing to do")
        send_telegram_message(    
    f"👋 *Hola!* \n\n"
    f"✅ *Tu clase fue reservada exitosamente!*\n\n"
    f"🏋️ *Clase:* {target_name}\n\n"
    f"🔥 ¡Echale bolas! 💪"
        )
        return

    try:
        client.book_class(target_day, _class["id"], family_id)
    except BookingFailed as e:
        if str(e) == MESSAGE_ALREADY_BOOKED_FOR_TIME:
            logger.error("You are already booked for this time")
            send_telegram_message("⚠️ Intente reservar, pero ya habias reservado!")
            return
        else:
            raise e

    logger.info("Class booked successfully")
    send_telegram_message(    
    f"👋 *Hola!* \n\n"
    f"✅ *Tu clase fue reservada exitosamente!*\n\n"
    f"🏋️ *Clase:* {target_name}\n\n"
    f"🔥 ¡Echale bolas! 💪"
    )


if __name__ == "__main__":
    email = os.environ["AH_USERNAME"]
    password = os.environ["AH_PASSWORD"]
    box_id = int(os.environ["AH_BOX_ID"])
    box_name = os.environ["AH_BOX_NAME"]

    parser = argparse.ArgumentParser()
    parser.add_argument("--booking-goals", required=True, type=json.loads)
    parser.add_argument("--days-in-advance", required=True, type=int, default=3)
    parser.add_argument(
        "--family-id",
        required=False,
        type=int,
        default=None,
        help="ID of the family member (optional)",
    )
    args = parser.parse_args()
    input = {
        "email": email,
        "password": password,
        "booking_goals": args.booking_goals,
        "box_name": box_name,
        "box_id": box_id,
        "days_in_advance": args.days_in_advance,
        "family_id": args.family_id,
    }
    main(**input)
