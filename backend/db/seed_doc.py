import pandas as pd

from backend.db.database import SessionLocal
from backend.db.models import Hospital, Department, Doctor

db = SessionLocal()

hospital = db.query(Hospital).first()

doctor_df = pd.read_excel(
    r"C:\Users\ASUS\OneDrive\Desktop\HOSPIITAL-BOT\data\doctors.xlsx"
)

print("Total Doctors in Excel:", len(doctor_df))

for _, row in doctor_df.iterrows():

    department = db.query(Department).filter(
        Department.dept_name == row["Department"]
    ).first()

    if department is None:
        print(f"Department not found: {row['Department']}")
        continue

    doctor = Doctor(
        hospital_id=hospital.id,
        dept_id=department.id,
        doctor_name=row["Doctor Name"],
        qualification=str(row["Qualification"]),
        designation=str(row["Designation"]),
        available_days=str(row["OP Days"]),
        max_tokens_per_day=40
    )

    db.add(doctor)

db.commit()

print("Doctors inserted successfully!")

db.close()