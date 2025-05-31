import tkinter as tk
from tkinter import messagebox
import requests
import smtplib
from email.message import EmailMessage
import sqlite3
import logging
import configparser
from datetime import datetime
from twilio.rest import Client
import pandas as pd

# ---------------- CONFIGURATION ----------------
config = configparser.ConfigParser()
config.read("config.ini")

API_KEY = config.get("weather", "api_key")
SENDER_EMAIL = config.get("email", "sender_email")
RECEIVER_EMAIL = config.get("email", "receiver_email")
SMTP_SERVER = config.get("email", "smtp_server")
SMTP_PORT = config.getint("email", "smtp_port")
LOGIN = config.get("email", "login")
PASSWORD = config.get("email", "password")

TWILIO_SID = config.get("twilio", "sid", fallback=None)
TWILIO_TOKEN = config.get("twilio", "auth_token", fallback=None)
TWILIO_FROM = config.get("twilio", "from_number", fallback=None)
TWILIO_TO = config.get("twilio", "to_number", fallback=None)

# ---------------- LOGGING ----------------
logging.basicConfig(
    filename="calculator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("history.db")
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        a REAL,
        op TEXT,
        b REAL,
        result REAL
    )"""
)
conn.commit()


# ---------------- CALCULATION ----------------
def calculate(a, b, op):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError("Invalid operation")


# ---------------- WEATHER ----------------
def get_weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


# ---------------- EMAIL ----------------
def send_email(subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.send_message(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Email Error:", e)


# ---------------- SMS (Twilio) ----------------
def send_sms(message):
    if TWILIO_SID and TWILIO_TOKEN and TWILIO_FROM and TWILIO_TO:
        try:
            client = Client(TWILIO_SID, TWILIO_TOKEN)
            msg = client.messages.create(body=message, from_=TWILIO_FROM, to=TWILIO_TO)
            print("✅ SMS sent:", msg.sid)
        except Exception as e:
            print("❌ SMS Error:", e)
    else:
        print("⚠ Twilio config missing, skipping SMS.")


# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Calculator & Weather App")


# -------- Calculator UI --------
tk.Label(root, text="First Number:").grid(row=0, column=0, padx=5, pady=5)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1)

tk.Label(root, text="Operation:").grid(row=1, column=0, padx=5, pady=5)
op_var = tk.StringVar(value="+")
op_menu = tk.OptionMenu(root, op_var, "+", "-", "*", "/")
op_menu.grid(row=1, column=1)

tk.Label(root, text="Second Number:").grid(row=2, column=0, padx=5, pady=5)
entry_b = tk.Entry(root)
entry_b.grid(row=2, column=1)

result_label = tk.Label(root, text="Result:")
result_label.grid(row=3, column=0, columnspan=2, pady=5)


def on_calculate():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        op = op_var.get()
        result = calculate(a, b, op)
        result_label.config(text=f"Result: {result}")
        logging.info(f"{a} {op} {b} = {result}")
        cursor.execute(
            "INSERT INTO operations (timestamp, a, op, b, result) VALUES (?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), a, op, b, result),
        )
        conn.commit()
    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        messagebox.showerror("Invalid Input", str(ve))
    except Exception as e:
        logging.error(f"Calculation error: {e}")
        messagebox.showerror("Error", str(e))


tk.Button(root, text="Calculate", command=on_calculate).grid(
    row=4, column=0, columnspan=2, pady=5
)

# -------- Weather UI --------
tk.Label(root, text="City for Weather:").grid(row=5, column=0, padx=5, pady=5)
entry_city = tk.Entry(root)
entry_city.grid(row=5, column=1)

weather_label = tk.Label(root, text="")
weather_label.grid(row=7, column=0, columnspan=2, pady=5)


def on_weather():
    try:
        city = entry_city.get()
        data = get_weather(city)
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        info = f"{city}: {desc}, {temp}°C"
        weather_label.config(text=info)
        send_email(f"Weather Update: {city}", info)
        send_sms(info)
        messagebox.showinfo("Success", "Weather sent via email and SMS.")
    except requests.HTTPError as he:
        logging.error(f"HTTP error: {he}")
        messagebox.showerror("HTTP Error", str(he))
    except Exception as e:
        logging.error(f"Weather/email error: {e}")
        messagebox.showerror("Error", str(e))


tk.Button(root, text="Get Weather & Email/SMS", command=on_weather).grid(
    row=6, column=0, columnspan=2, pady=5
)


# -------- Report Generator --------
def generate_report():
    try:
        df = pd.read_sql_query("SELECT * FROM operations", conn)
        df.to_csv("calculation_report.csv", index=False)
        messagebox.showinfo("Report", "Report saved as calculation_report.csv")
    except Exception as e:
        logging.error(f"Report error: {e}")
        messagebox.showerror("Report Error", str(e))


tk.Button(root, text="Generate Report", command=generate_report).grid(
    row=8, column=0, columnspan=2, pady=5
)

# -------- Start GUI --------
root.mainloop()
