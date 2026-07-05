import pandas as pd

from backend.db.database import SessionLocal
from backend.db.models import Hospital, Department

db = SessionLocal()

hospital = db.query(Hospital).first()

department_df = pd.read_excel(
    r"C:\Users\ASUS\OneDrive\Desktop\HOSPIITAL-BOT\data\departments.xlsx"
)

for _, row in department_df.iterrows():

    department = Department(
        hospital_id=hospital.id,
        dept_name=row["Department Name"],
        dept_code=row["Department Name"][:3].upper()
    )

    db.add(department)

db.commit()

print("Departments inserted successfully!")

db.close()