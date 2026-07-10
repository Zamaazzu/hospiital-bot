from backend.db.database import SessionLocal
from backend.db.models import Hospital, Department


def lookup_hospital_info(hospital_name=None):
    db = SessionLocal()
    try:
        query = db.query(Hospital)
        if hospital_name:
            query = query.filter(Hospital.name == hospital_name)

        hospital = query.first()

        if not hospital:
            return {
                "hospital_name": None,
                "address": None,
                "contact": None,
                "departments": []
            }

        departments = (
            db.query(Department)
            .filter(Department.hospital_id == hospital.id)
            .all()
        )

        return {
            "hospital_name": hospital.name,
            "address": hospital.address,
            "contact": hospital.phone,
            "departments": [d.dept_name for d in departments]
        }

    except Exception as e:
        print("Hospital lookup failed:", e)
        return {}

    finally:
        db.close()