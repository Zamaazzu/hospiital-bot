from backend.db.database import SessionLocal
from backend.db.models import Doctor, Department, OPSchedule
from datetime import date as current_date, timedelta

WEEKDAYS = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
}

def lookup_available_doctors(department=None, doctor=None, date=None):
    db = SessionLocal()
    try:
        query = (
            db.query(Doctor, Department, OPSchedule)
            .join(Department, Doctor.dept_id == Department.id)
            .join(OPSchedule, Doctor.id == OPSchedule.doctor_id)
        )
        if department:
            query = query.filter(Department.dept_name == department)
        if doctor:
            query = query.filter(Doctor.doctor_name == doctor)

        if date:
            date_lower = date.lower() if isinstance(date, str) else date

            if date_lower == "today":
                date = current_date.today()
            elif date_lower == "tomorrow":
                date = current_date.today() + timedelta(days=1)
            elif isinstance(date_lower, str) and date_lower in WEEKDAYS:
                today = current_date.today()
                target = WEEKDAYS[date_lower]
                days_ahead = (target - today.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7
                date = today + timedelta(days=days_ahead)

            query = query.filter(OPSchedule.schedule_date == date)

        results = query.all()

        doctor_list = []
        for doctor_obj, department_obj, schedule_obj in results:
            doctor_list.append({
                "doctor_name": doctor_obj.doctor_name,
                "department": department_obj.dept_name,
                "time": f"{schedule_obj.start_time} - {schedule_obj.end_time}",
                "tokens_left": schedule_obj.total_tokens - schedule_obj.tokens_issued
            })

        return doctor_list

    except Exception as e:
        print(f"Doctor lookup failed: {e}")
        return []

    finally:
        db.close()

def get_all_doctors(department_id=None):
    db = SessionLocal()
    try:
        query = (
            db.query(Doctor, Department, OPSchedule)
            .join(Department, Doctor.dept_id == Department.id)
            .join(OPSchedule, Doctor.id == OPSchedule.doctor_id)
        )
        if department_id:
            query = query.filter(Department.id == department_id)

        results = query.all()

        doctor_list = []
        for doctor_obj, department_obj, schedule_obj in results:
            doctor_list.append({
                "schedule_id": schedule_obj.id,
                "doctor_id": doctor_obj.id,
                "doctor_name": doctor_obj.doctor_name,
                "department": department_obj.dept_name,
                "tokens_left": schedule_obj.total_tokens - schedule_obj.tokens_issued,
                "total_tokens": schedule_obj.total_tokens,
                "report_time": f"{schedule_obj.start_time.strftime('%I:%M %p')} - {schedule_obj.end_time.strftime('%I:%M %p')}"
            })

        return doctor_list

    except Exception as e:
        print(f"Doctor lookup failed: {e}")
        return []
    finally:
        db.close()

def get_doctor_details(doctor_id):
    db = SessionLocal()
    try:
        doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

        if not doctor:
            return {}

        schedules = (
            db.query(OPSchedule)
            .filter(OPSchedule.doctor_id == doctor_id)
            .order_by(OPSchedule.schedule_date,OPSchedule.start_time)
            .all()
        )

        schedule_list = [
            {
                "schedule_id": s.id,
                "date": str(s.schedule_date),
                "report_time": f"{s.start_time.strftime('%I:%M %p')} - {s.end_time.strftime('%I:%M %p')}",
                "tokens_left": s.total_tokens - s.tokens_issued,
                "total_tokens": s.total_tokens,
                "status": s.status
            }
            for s in schedules
        ]

        return {
            "doctor_id": doctor.id,
            "doctor_name": doctor.doctor_name,
            "qualification": doctor.qualification,
            "designation": doctor.designation,
            "department": doctor.department.dept_name,
            "hospital": doctor.hospital.name,
            "available_days": doctor.available_days,
            "schedules": schedule_list
        }

    except Exception as e:
        print(f"Doctor details lookup failed: {e}")
        return {}

    finally:
        db.close()

def get_available_tokens(doctor_id):
    db = SessionLocal()
    try:
        schedules = (
            db.query(OPSchedule)
            .filter(OPSchedule.doctor_id == doctor_id)
            .filter(OPSchedule.status == "available")
            .order_by(OPSchedule.schedule_date, OPSchedule.start_time)
            .all()
        )

        if not schedules:
            return []

        return [
            {
                "schedule_id": s.id,
                "date": str(s.schedule_date),
                "report_time": f"{s.start_time.strftime('%I:%M %p')} - {s.end_time.strftime('%I:%M %p')}",
                "tokens_left": s.total_tokens - s.tokens_issued,
                "total_tokens": s.total_tokens
            }
            for s in schedules
        ]

    except Exception as e:
        print(f"Available tokens lookup failed: {e}")
        return []

    finally:
        db.close()