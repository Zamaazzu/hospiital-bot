from sqlalchemy import Column, Integer, String, ForeignKey,Date,Time,DateTime
from sqlalchemy.orm import relationship
from .database import Base
class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(String(300))
    district = Column(String(100))
    phone = Column(String(20))
    type = Column(String(20))
    departments = relationship("Department", back_populates="hospital")
    doctors = relationship("Doctor", back_populates="hospital")
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    dept_name = Column(String(100), nullable=False)
    dept_code = Column(String(20), nullable=False)

    hospital = relationship("Hospital", back_populates="departments")
    doctors = relationship("Doctor", back_populates="department")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    dept_id = Column(Integer, ForeignKey("departments.id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))

    doctor_name = Column(String(150), nullable=False)
    qualification = Column(String(100))
    available_days = Column(String(100))
    max_tokens_per_day = Column(Integer)

    hospital = relationship("Hospital", back_populates="doctors")
    department = relationship("Department", back_populates="doctors")
    op_schedules = relationship("OPSchedule", back_populates="doctor")


class OPSchedule(Base):
    __tablename__ = "op_schedules"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    schedule_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    total_tokens = Column(Integer, nullable=False)
    tokens_issued = Column(Integer, default=0)

    status = Column(String(20), default="available")

    doctor = relationship("Doctor", back_populates="op_schedules")
    op_tokens = relationship("OPToken", back_populates="schedule")


class OPToken(Base):
    __tablename__ = "op_tokens"

    id = Column(Integer, primary_key=True, index=True)

    schedule_id = Column(Integer, ForeignKey("op_schedules.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))

    token_number = Column(String(50), unique=True, nullable=False)

    booking_time = Column(DateTime)

    status = Column(String(20), default="waiting")

    schedule = relationship("OPSchedule", back_populates="op_tokens")
    patient = relationship("Patient", back_populates="op_tokens")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(20))
    phone = Column(String(20))
    address = Column(String(300))

    op_tokens = relationship("OPToken", back_populates="patient")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String(100), unique=True, nullable=False)

    last_intent = Column(String(100))

    last_doctor_id = Column(Integer, ForeignKey("doctors.id"))

    last_schedule_id = Column(Integer, ForeignKey("op_schedules.id"))

    created_at = Column(DateTime)

    doctor = relationship("Doctor")
    schedule = relationship("OPSchedule")