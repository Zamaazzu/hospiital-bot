from backend.db.database import SessionLocal
from backend.db.models import Department


def get_departments():
    db = SessionLocal()
    try:
        departments = db.query(Department).order_by(Department.dept_name).all()

        return [
            {
                "department_id": dept.id,
                "department": dept.dept_name,
                "dept_code": dept.dept_code
            }
            for dept in departments
        ]

    except Exception as e:
        print(f"Department lookup failed: {e}")
        return []

    finally:
        db.close()


def get_department_by_name(name):
    db = SessionLocal()
    try:
        dept = db.query(Department).filter(Department.dept_name == name).first()
        if not dept:
            return None
        return {"department_id": dept.id, "department_name": dept.dept_name}
    except Exception as e:
        print(f"Department name lookup failed: {e}")
        return None
    finally:
        db.close()