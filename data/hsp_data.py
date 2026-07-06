import pandas as pd
import random
from datetime import datetime, timedelta

# Read doctors
doctor_df = pd.read_excel(
    r"C:\Users\ASUS\OneDrive\Desktop\HOSPIITAL-BOT\data\doctors.xlsx"
)

# Tomorrow's date
schedule_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

# Select 3 random doctors on leave
leave_doctors = random.sample(
    list(doctor_df["Doctor Name"]),
    3
)

schedule = []

for _, row in doctor_df.iterrows():

    doctor_name = row["Doctor Name"]

    if doctor_name in leave_doctors:
        status = "leave"
    else:
        status = "available"

    schedule.append({
        "Doctor Name": doctor_name,
        "Schedule Date": schedule_date,
        "Start Time": "09:00:00",
        "End Time": "17:00:00",
        "Total Tokens": 40,
        "Tokens Issued": 0,
        "Status": status
    })

schedule_df = pd.DataFrame(schedule)

schedule_df.to_excel(
    r"C:\Users\ASUS\OneDrive\Desktop\HOSPIITAL-BOT\data\op_schedule.xlsx",
    index=False
)

print("OP Schedule created successfully!")
print("Total schedules:", len(schedule_df))

print("\nDoctors on Leave:")
for doctor in leave_doctors:
    print(doctor)

print("\nFirst 5 Rows:")
print(schedule_df.head())