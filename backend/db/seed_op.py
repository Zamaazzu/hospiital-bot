import pandas as pd
from datetime import datetime

from backend.db.database import SessionLocal
from backend.db.models import Doctor, OPSchedule

db = SessionLocal()

# Read Excel
schedule_df = pd.read_excel(
    r"C:\Users\ASUS\OneDrive\Desktop\HOSPIITAL-BOT\data\op_schedule.xlsx"
)

print("Total Schedules:", len(schedule_df))

for _, row in schedule_df.iterrows():

    # Find doctor using doctor name
    doctor = db.query(Doctor).filter(
        Doctor.doctor_name == row["Doctor Name"]
    ).first()

    if doctor is None:
        print(f"Doctor not found: {row['Doctor Name']}")
        continue

    schedule = OPSchedule(
        doctor_id=doctor.id,
        schedule_date=pd.to_datetime(row["Schedule Date"]).date(),
        start_time=pd.to_datetime(row["Start Time"]).time(),
        end_time=pd.to_datetime(row["End Time"]).time(),
        total_tokens=int(row["Total Tokens"]),
        tokens_issued=int(row["Tokens Issued"]),
        status=row["Status"]
    )

    db.add(schedule)

db.commit()

print("OP Schedules inserted successfully!")

db.close()