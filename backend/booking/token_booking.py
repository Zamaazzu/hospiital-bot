from datetime import datetime,timedelta

from backend.db.database import SessionLocal
from backend.db.models import (
    Doctor,
    OPSchedule,
    OPToken,
    Patient
)
def _generate_token_number(schedule):
    dept_code = schedule.doctor.department.dept_code
    date_str = schedule.schedule_date.strftime("%Y%m%d")
    sequence = schedule.tokens_issued + 1
    return f"{dept_code}-{date_str}-{sequence:03d}"
def book_token(schedule_id, name, phone=None, age=None, gender=None):
    db = SessionLocal()
    try:
        schedule = (
            db.query(OPSchedule)
            .filter(OPSchedule.id == schedule_id)
            .first()
        )
        if not schedule:
            return {"success": False, "message": "Schedule not found"}

        if schedule.tokens_issued >= schedule.total_tokens:
            return {"success": False, "message": "No tokens are available for this schedule"}

        patient = Patient(name=name, age=age, gender=gender, phone=phone)
        db.add(patient)
        db.flush()

        token_number = _generate_token_number(schedule)
        new_token = OPToken(
            schedule_id=schedule_id,
            patient_id=patient.id,
            token_number=token_number,
            booking_time=datetime.now(),
            status="Booked"
        )
        db.add(new_token)
        schedule.tokens_issued += 1
        db.commit()
        db.refresh(new_token)

        doctor = schedule.doctor
        department = doctor.department
        hospital = doctor.hospital

        return {
            "success": True,
            "token_number": new_token.token_number,
            "status": new_token.status,
            "doctor_name": doctor.doctor_name,
            "department": department.dept_name,
            "hospital": hospital.name,
            "date": str(schedule.schedule_date),
            "report_time": str(schedule.start_time),
            "booking_time": new_token.booking_time.isoformat()
        }
    except Exception as e:
        db.rollback()
        print(f"Booking error: {e}")
        return {
            "success": False,
            "message": "Booking failed. Please try again."
        }
    finally:
        db.close()

def _calculate_estimated_time(schedule, token_number):
    average_consultation_minutes = 10
    sequence = int(token_number.split("-")[-1])

    estimated_time = (
        datetime.combine(datetime.today(), schedule.start_time)
        + timedelta(minutes=(sequence - 1) * average_consultation_minutes)
    ).time()

    return estimated_time
def get_token_status(token_number):
    db=SessionLocal()
    try:
        token=(
            db.query(OPToken)
            .filter(OPToken.token_number==token_number)
            .first()
        )
        if not token:
            return {
                "success": False,
                "message": "Token not found."
            }
        schedule = (
                db.query(OPSchedule)
                .filter(OPSchedule.id == token.schedule_id)
                .first()
        ) 
        doctor = (
            db.query(Doctor)
            .filter(Doctor.id == schedule.doctor_id)
            .first()
        )
        
        estimated_time=_calculate_estimated_time(schedule,token.token_number)
        return {
            "success": True,
            "token_number": token.token_number,
            "doctor_name": doctor.doctor_name,
            "department": doctor.department.dept_name,
            "date": str(schedule.schedule_date),
            "status": token.status,
            "estimated_time": estimated_time.strftime("%I:%M %p")
        }
    except Exception as e:
        db.rollback()
        return {
                "success": False,
                "message": str(e)
    }
    finally:
        db.close()