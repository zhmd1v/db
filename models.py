# models.py
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, Date, Time, Float, ForeignKey, DateTime

Base = declarative_base()

class User(Base):
    __tablename__ = "user"   # make sure this matches your real table name

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100))
    phone_number = Column(String(30))
    profile_description = Column(Text)
    password = Column(String(255), nullable=False)

    caregiver = relationship("Caregiver", back_populates="user", uselist=False)
    member = relationship("Member", back_populates="user", uselist=False)

class Caregiver(Base):
    __tablename__ = "caregiver"

    caregiver_user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    photo = Column(String(255))
    gender = Column(String(10))
    caregiving_type = Column(String(50))  # babysitter / elderly / playmate
    hourly_rate = Column(Float)

    user = relationship("User", back_populates="caregiver")
    job_applications = relationship("JobApplication", back_populates="caregiver")
    appointments = relationship("Appointment", back_populates="caregiver")

class Member(Base):
    __tablename__ = "member"

    member_user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    house_rules = Column(Text)
    dependent_description = Column(Text)

    user = relationship("User", back_populates="member")
    address = relationship("Address", back_populates="member", uselist=False)
    jobs = relationship("Job", back_populates="member")
    appointments = relationship("Appointment", back_populates="member")

class Address(Base):
    __tablename__ = "address"

    member_user_id = Column(Integer, ForeignKey("member.member_user_id"), primary_key=True)
    house_number = Column(String(50))
    street = Column(String(200))
    town = Column(String(100))

    member = relationship("Member", back_populates="address")

class Job(Base):
    __tablename__ = "job"

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    member_user_id = Column(Integer, ForeignKey("member.member_user_id"), nullable=False)
    required_caregiving_type = Column(String(50))
    other_requirements = Column(Text)
    date_posted = Column(Date)

    member = relationship("Member", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")

class JobApplication(Base):
    __tablename__ = "job_application"

    caregiver_user_id = Column(Integer, ForeignKey("caregiver.caregiver_user_id"), primary_key=True)
    job_id = Column(Integer, ForeignKey("job.job_id"), primary_key=True)
    date_applied = Column(Date)

    caregiver = relationship("Caregiver", back_populates="job_applications")
    job = relationship("Job", back_populates="applications")

class Appointment(Base):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    caregiver_user_id = Column(Integer, ForeignKey("caregiver.caregiver_user_id"), nullable=False)
    member_user_id = Column(Integer, ForeignKey("member.member_user_id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(Integer, nullable=False)
    status = Column(String(20))   # pending / accepted / declined

    caregiver = relationship("Caregiver", back_populates="appointments")
    member = relationship("Member", back_populates="appointments")
