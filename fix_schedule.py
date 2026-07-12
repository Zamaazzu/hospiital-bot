from backend.db.database import SessionLocal
from backend.db.models import OPSchedule
from datetime import date, timedelta

db = SessionLocal()

schedules = db.query(OPSchedule).all()
today = date.today()

for i, schedule in enumerate(schedules):
    offset = i % 5
    schedule.schedule_date = today + timedelta(days=offset)

db.commit()
db.close()

print(f"Updated {len(schedules)} schedules with dates spread across {today} to {today + timedelta(days=4)}")