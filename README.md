# Weather Calculator Project
📌 Project Description

The Weather Calculator Project is a Python-based application that combines two core utilities:

A Basic Arithmetic Calculator

Perform operations like addition, subtraction, multiplication, and division.

Built using Tkinter GUI for user-friendly interaction.

Handles errors such as division by zero and invalid inputs.

Supports decimal and integer values.

Stores operation history.

Live Weather Report Sender

Fetches real-time weather data using the OpenWeatherMap API.

Sends daily weather updates via Email and/or SMS using SMTP and Twilio API.

Designed to be configurable via a secure config.ini file.

This project showcases an integration of GUI development, API consumption, email and SMS automation, and configuration management.

✅ Features Implemented

✔️ Tkinter GUI-based Calculator

✔️ Arithmetic operations with error handling

✔️ Decimal & integer input support

✔️ SQLite database for storing calculation history

✔️ Email weather update using SMTP

✔️ SMS weather update using Twilio (optional)

✔️ Secure and customizable via config.ini

✔️ Modular and well-documented code
---
🔧 How to Configure config.ini
Before running the project, update all REDACTED values in config.ini with your personal credentials. Follow the steps below to configure each section correctly.

📧 [EMAIL] Section – Send Weather Updates via Email
```
sender_email = REDACTED
receiver_email = REDACTED
smtp_server = REDACTED
smtp_port = 465
login = REDACTED
password = REDACTED
```
🔹 How to get these values:

sender_email: Your email address (e.g., your_email@gmail.com)

receiver_email: Email where the weather update should be sent.

smtp_server:

Gmail: smtp.gmail.com

Outlook: smtp.office365.com

Yahoo: smtp.mail.yahoo.com

smtp_port: Usually 465 (SSL) or 587 (TLS)

login: Usually same as sender_email

password:

⚠️ Use an App Password instead of your email login password

For Gmail:

Go to your Google Account

Enable 2-Step Verification

Visit App Passwords

Generate one for “Mail” and use it here

🌤️ [WEATHER] Section – Fetch Live Weather Data
```
[WEATHER]
api_key = REDACTED
location = REDACTED
```
🔹 How to get these values:

api_key:

Sign up at OpenWeatherMap

Go to your API Keys Page

Copy your default key

location:

City name like New York, Delhi, London

📲 [twilio] Section – Send Weather Updates via SMS
```
[twilio]
sid = REDACTED
auth_token = REDACTED
from_number = REDACTED
to_number = REDACTED
```
🔹 How to get these values:

sid & auth_token:

Sign up at Twilio

Go to Twilio Console

Copy the Account SID and Auth Token

from_number:
Your Twilio phone number (must be SMS-enabled)

to_number:
Your verified mobile number (e.g., +15551234567)

Note: Trial accounts must verify the destination number
---
🛑 Important Security Note
⚠️ Do NOT share your real config.ini or credentials publicly.

Keep config.ini private or add it to .gitignore.

Consider using .env files and the python-dotenv package for more security in deployment.
---
🚀 How to Run

1.Clone the repository:
```
git clone https://github.com/Akhila-1703/Weather_Calculator_Project.git
cd Weather_Calculator_Project
```
2.Install dependencies (if any):
```
pip install -r requirements.txt
```
3.Update config.ini with your credentials (see instructions above).

4.Run the application:
```
python main.py
```
---
 🛠️ Found a bug? Have a feature request? Feel free to open an issue or submit a pull request.
 
📬 For questions or feedback, email: akhiladhachepally@gmail.com

🙏  Thank you for using this Application!
