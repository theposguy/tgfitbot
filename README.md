Thanks! Here's the **updated GitHub description** based on the new implementation, which runs via **GitHub Actions**, includes **Telegram notifications**, uses environment **secrets**, and removes Docker/Raspberry Pi dependencies:

---

## 🐝 FitBot · AimHarder Booking Automation

Automated class booking bot for the [aimharder.com](https://www.aimharder.com) platform — now modernized to run entirely through **GitHub Actions** with **Telegram notifications**.

---

### ✅ Features

* Automatically books your training classes based on your custom schedule.
* Sends Telegram messages upon successful bookings or if something goes wrong.
* Runs on a set schedule (no Raspberry Pi or Docker needed!).
* Configuration is handled entirely through GitHub **Secrets**.

---

### 🛠️ Setup

1. **Fork this repository.**
2. Go to your repository **Settings > Secrets and variables > Actions > Secrets** and add the following secrets:

| Secret Name             | Description                                                       |
| ----------------------- | ----------------------------------------------------------------- |
| `AH_USERNAME`           | Your AimHarder email                                              |
| `AH_PASSWORD`           | Your AimHarder password                                           |
| `AH_BOX_ID`             | Box ID (gym ID - find via browser DevTools when booking manually) |
| `AH_BOX_NAME`           | Subdomain of your gym, e.g., `lahuellacrossfit`                   |
| `BOOKING_GOALS`         | JSON with class time/name goals (see example below)               |
| `HOURS_IN_ADVANCE`      | How many hours in advance the class becomes available for booking |
| `AH_TELEGRAM_BOT_TOKEN` | Token from [@BotFather](https://t.me/BotFather)                   |
| `AH_CHAT_ID`            | Your Telegram user ID (use a bot to get it, e.g., @userinfobot)   |

---

`AH_BOX_ID`: it's always the same one for your gym, you can find it inspecting the request made while booking a class from the browser:

<img src="https://raw.github.com/pablobuenaposada/fitbot/master/inspect.png" data-canonical-src="https://raw.github.com/pablobuenaposada/fitbot/master/inspect.png" height="300" />

---

### 🧠 Booking Goals Format

The `BOOKING_GOALS` secret should contain a JSON like this:

```json
{
  "0": {"time": "0700", "name": "CrossFit"},
  "2": {"time": "0700", "name": "Bike Class"},
  "4": {"time": "0700", "name": "Row Class"}
}
```

Where:

* `"0"` is Monday, `"2"` is Wednesday, `"4"` is Friday.
* `"time"` is the class time in 24h format (`HHMM`).
* `"name"` is part or all of the class name.

---

### 🕒 Schedule

By default, the GitHub Actions workflow runs on:

* Sunday, Tuesday, and Thursday
* At **8:45 AM Venezuela time** (13:45 UTC)

You can adjust this in `.github/workflows/fitbot.yml` using the `cron` field.

---

### 💬 Telegram Notifications

You’ll get messages like this when a class is successfully booked:

```
👋 Hello @YourUsername!
✅ Your class was successfully booked:

🕐 Time: Monday, May 12 at 07:00 (VET)
🏋️ Class: Crossfit Muscle

💪 Keep it up!
```

If something fails, the bot will also notify you with error info.

---

### ✅ Want to Test It?

You can trigger the bot manually via the "Actions" tab in GitHub and selecting **"Run workflow"**.

---

Enjoy your workouts, now with less stress and more automation! 💪🤖

---
