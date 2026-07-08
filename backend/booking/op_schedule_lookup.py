from backend.db.database import SessionLocal
from backend.db.models import Doctor,Department,OPSchedule
def lookup_available_doctors(department=None,doctor=None,date=None):
    db=SessionLocal()
    query = (
    db.query(Doctor, Department, OPSchedule)
    .join(Department, Doctor.dept_id == Department.id)
    .join(OPSchedule, Doctor.id == OPSchedule.doctor_id)
    )
    if department:
        query=query.filter(Department.dept_name==department)
    if doctor:
        query = query.filter(Doctor.doctor_name == doctor)

    if date:
        query = query.filter(OPSchedule.schedule_date == date)

    results=query.all() 

    doctor_list = []

    for doctor_obj, department_obj, schedule_obj in results:

        doctor_list.append({
            "doctor_name": doctor_obj.doctor_name,
            "department": department_obj.dept_name,
            "time": f"{schedule_obj.start_time} - {schedule_obj.end_time}",
            "tokens_left": schedule_obj.total_tokens - schedule_obj.tokens_issued
        })
    db.close()
    return doctor_list