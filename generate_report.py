import sqlite3
import pandas as pd


def generate_csv_report():
    conn = sqlite3.connect("history.db")
    df = pd.read_sql_query("SELECT * FROM calculations", conn)
    df.to_csv("calculator_report.csv", index=False)
    conn.close()
    print("Report generated: calculator_report.csv")
