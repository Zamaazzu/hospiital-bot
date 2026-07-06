import pandas as pd

from backend.db.database import SessionLocal
from backend.db.models import Hospital

db = SessionLocal()

hospital_df = pd.read_excel(
    r"C:\Users\ASUS\OneDrive\Desktop\HOSPIITAL-BOT\data\hospital.xlsx"
)

for _, row in hospital_df.iterrows():

    hospital = Hospital(
        name=row["Hospital Name"],
        address=row["Address"],
        district=row["District"],
        phone=str(row["Phone"]),
        type=row["Type"]
    )

    db.add(hospital)

db.commit()

print("Hospital inserted successfully!")

db.close()