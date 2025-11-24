# app.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

from db_config import SessionLocal, engine
from models import (
    Base,
    User,
    Caregiver,
    Member,
    Address,
    Job,
    JobApplication,
    Appointment,
)

app = Flask(__name__)

# Create tables if they don't exist yet (optional – your DB likely has them already)
#Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

####user crud

@app.route("/users")
def list_users():
    db = next(get_db())
    users = db.query(User).all()
    return render_template("users_list.html", users=users)


@app.route("/users/create", methods=["GET", "POST"])
def create_user():
    db = next(get_db())
    if request.method == "POST":
        new_user = User(
            email=request.form["email"],
            given_name=request.form["given_name"],
            surname=request.form["surname"],
            city=request.form.get("city"),
            phone_number=request.form.get("phone_number"),
            profile_description=request.form.get("profile_description"),
            password=request.form["password"],
        )
        db.add(new_user)
        db.commit()
        return redirect(url_for("list_users"))
    return render_template("user_form.html", user=None, action="create")


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user(user_id):
    db = next(get_db())
    user = db.query(User).get(user_id)
    if not user:
        return "User not found", 404

    if request.method == "POST":
        user.email = request.form["email"]
        user.given_name = request.form["given_name"]
        user.surname = request.form["surname"]
        user.city = request.form.get("city")
        user.phone_number = request.form.get("phone_number")
        user.profile_description = request.form.get("profile_description")
        user.password = request.form["password"]
        db.commit()
        return redirect(url_for("list_users"))

    return render_template("user_form.html", user=user, action="edit")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    db = next(get_db())
    user = db.query(User).get(user_id)
    if not user:
        return "User not found", 404
    db.delete(user)
    db.commit()
    return redirect(url_for("list_users"))


###caregivers crud

@app.route("/caregivers")
def list_caregivers():
    db = next(get_db())
    caregivers = db.query(Caregiver).all()
    return render_template("caregivers_list.html", caregivers=caregivers)


@app.route("/caregivers/create", methods=["GET", "POST"])
def create_caregiver():
    db = next(get_db())
    if request.method == "POST":
        caregiver = Caregiver(
            caregiver_user_id=int(request.form["caregiver_user_id"]),
            photo=request.form.get("photo"),
            gender=request.form.get("gender"),
            caregiving_type=request.form.get("caregiving_type"),
            hourly_rate=float(request.form.get("hourly_rate") or 0),
        )
        db.add(caregiver)
        db.commit()
        return redirect(url_for("list_caregivers"))

    users = db.query(User).all()
    return render_template("caregiver_form.html", caregiver=None, users=users, action="create")


@app.route("/caregivers/<int:caregiver_user_id>/edit", methods=["GET", "POST"])
def edit_caregiver(caregiver_user_id):
    db = next(get_db())
    caregiver = db.query(Caregiver).get(caregiver_user_id)
    if not caregiver:
        return "Caregiver not found", 404

    if request.method == "POST":
        caregiver.photo = request.form.get("photo")
        caregiver.gender = request.form.get("gender")
        caregiver.caregiving_type = request.form.get("caregiving_type")
        caregiver.hourly_rate = float(request.form.get("hourly_rate") or 0)
        db.commit()
        return redirect(url_for("list_caregivers"))

    users = db.query(User).all()
    return render_template("caregiver_form.html", caregiver=caregiver, users=users, action="edit")


@app.route("/caregivers/<int:caregiver_user_id>/delete", methods=["POST"])
def delete_caregiver(caregiver_user_id):
    db = next(get_db())
    caregiver = db.query(Caregiver).get(caregiver_user_id)
    if not caregiver:
        return "Caregiver not found", 404
    db.delete(caregiver)
    db.commit()
    return redirect(url_for("list_caregivers"))


####member crud

@app.route("/members")
def list_members():
    db = next(get_db())
    members = db.query(Member).all()
    return render_template("members_list.html", members=members)


@app.route("/members/create", methods=["GET", "POST"])
def create_member():
    db = next(get_db())
    if request.method == "POST":
        member = Member(
            member_user_id=int(request.form["member_user_id"]),
            house_rules=request.form.get("house_rules"),
            dependent_description=request.form.get("dependent_description"),
        )
        db.add(member)
        db.commit()
        return redirect(url_for("list_members"))

    users = db.query(User).all()
    return render_template("member_form.html", member=None, users=users, action="create")


@app.route("/members/<int:member_user_id>/edit", methods=["GET", "POST"])
def edit_member(member_user_id):
    db = next(get_db())
    member = db.query(Member).get(member_user_id)
    if not member:
        return "Member not found", 404

    if request.method == "POST":
        member.house_rules = request.form.get("house_rules")
        member.dependent_description = request.form.get("dependent_description")
        db.commit()
        return redirect(url_for("list_members"))

    users = db.query(User).all()
    return render_template("member_form.html", member=member, users=users, action="edit")


@app.route("/members/<int:member_user_id>/delete", methods=["POST"])
def delete_member(member_user_id):
    db = next(get_db())
    member = db.query(Member).get(member_user_id)
    if not member:
        return "Member not found", 404
    db.delete(member)
    db.commit()
    return redirect(url_for("list_members"))


####address crud

@app.route("/addresses")
def list_addresses():
    db = next(get_db())
    addresses = db.query(Address).all()
    return render_template("addresses_list.html", addresses=addresses)


@app.route("/addresses/create", methods=["GET", "POST"])
def create_address():
    db = next(get_db())
    if request.method == "POST":
        addr = Address(
            member_user_id=int(request.form["member_user_id"]),
            house_number=request.form.get("house_number"),
            street=request.form.get("street"),
            town=request.form.get("town"),
        )
        db.add(addr)
        db.commit()
        return redirect(url_for("list_addresses"))

    members = db.query(Member).all()
    return render_template("address_form.html", address=None, members=members, action="create")


@app.route("/addresses/<int:member_user_id>/edit", methods=["GET", "POST"])
def edit_address(member_user_id):
    db = next(get_db())
    addr = db.query(Address).get(member_user_id)
    if not addr:
        return "Address not found", 404

    if request.method == "POST":
        addr.house_number = request.form.get("house_number")
        addr.street = request.form.get("street")
        addr.town = request.form.get("town")
        db.commit()
        return redirect(url_for("list_addresses"))

    members = db.query(Member).all()
    return render_template("address_form.html", address=addr, members=members, action="edit")


@app.route("/addresses/<int:member_user_id>/delete", methods=["POST"])
def delete_address(member_user_id):
    db = next(get_db())
    addr = db.query(Address).get(member_user_id)
    if not addr:
        return "Address not found", 404
    db.delete(addr)
    db.commit()
    return redirect(url_for("list_addresses"))


### job crud

@app.route("/jobs")
def list_jobs():
    db = next(get_db())
    jobs = db.query(Job).all()
    return render_template("jobs_list.html", jobs=jobs)


@app.route("/jobs/create", methods=["GET", "POST"])
def create_job():
    db = next(get_db())
    if request.method == "POST":
        date_str = request.form.get("date_posted")
        date_posted = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        job = Job(
            member_user_id=int(request.form["member_user_id"]),
            required_caregiving_type=request.form.get("required_caregiving_type"),
            other_requirements=request.form.get("other_requirements"),
            date_posted=date_posted,
        )
        db.add(job)
        db.commit()
        return redirect(url_for("list_jobs"))

    members = db.query(Member).all()
    return render_template("job_form.html", job=None, members=members, action="create")


@app.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
def edit_job(job_id):
    db = next(get_db())
    job = db.query(Job).get(job_id)
    if not job:
        return "Job not found", 404

    if request.method == "POST":
        date_str = request.form.get("date_posted")
        job.member_user_id = int(request.form["member_user_id"])
        job.required_caregiving_type = request.form.get("required_caregiving_type")
        job.other_requirements = request.form.get("other_requirements")
        job.date_posted = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        db.commit()
        return redirect(url_for("list_jobs"))

    members = db.query(Member).all()
    return render_template("job_form.html", job=job, members=members, action="edit")


@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):
    db = next(get_db())
    job = db.query(Job).get(job_id)
    if not job:
        return "Job not found", 404
    db.delete(job)
    db.commit()
    return redirect(url_for("list_jobs"))


### job application crud

@app.route("/job_applications")
def list_job_applications():
    db = next(get_db())
    apps = db.query(JobApplication).all()
    return render_template("job_applications_list.html", applications=apps)


@app.route("/job_applications/create", methods=["GET", "POST"])
def create_job_application():
    db = next(get_db())
    if request.method == "POST":
        date_str = request.form.get("date_applied")
        date_applied = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        app_obj = JobApplication(
            caregiver_user_id=int(request.form["caregiver_user_id"]),
            job_id=int(request.form["job_id"]),
            date_applied=date_applied,
        )
        db.add(app_obj)
        db.commit()
        return redirect(url_for("list_job_applications"))

    caregivers = db.query(Caregiver).all()
    jobs = db.query(Job).all()
    return render_template(
        "job_application_form.html",
        application=None,
        caregivers=caregivers,
        jobs=jobs,
        action="create",
    )


@app.route("/job_applications/<int:caregiver_user_id>/<int:job_id>/edit", methods=["GET", "POST"])
def edit_job_application(caregiver_user_id, job_id):
    db = next(get_db())
    app_obj = db.query(JobApplication).get((caregiver_user_id, job_id))
    if not app_obj:
        return "Job application not found", 404

    if request.method == "POST":
        date_str = request.form.get("date_applied")
        app_obj.date_applied = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        db.commit()
        return redirect(url_for("list_job_applications"))

    caregivers = db.query(Caregiver).all()
    jobs = db.query(Job).all()
    return render_template(
        "job_application_form.html",
        application=app_obj,
        caregivers=caregivers,
        jobs=jobs,
        action="edit",
    )


@app.route("/job_applications/<int:caregiver_user_id>/<int:job_id>/delete", methods=["POST"])
def delete_job_application(caregiver_user_id, job_id):
    db = next(get_db())
    app_obj = db.query(JobApplication).get((caregiver_user_id, job_id))
    if not app_obj:
        return "Job application not found", 404
    db.delete(app_obj)
    db.commit()
    return redirect(url_for("list_job_applications"))


#### appointment crud

@app.route("/appointments")
def list_appointments():
    db = next(get_db())
    appointments = db.query(Appointment).all()
    return render_template("appointments_list.html", appointments=appointments)


@app.route("/appointments/create", methods=["GET", "POST"])
def create_appointment():
    db = next(get_db())
    if request.method == "POST":
        date_str = request.form.get("appointment_date")
        time_str = request.form.get("appointment_time")

        appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        appointment_time = datetime.strptime(time_str, "%H:%M").time() if time_str else None

        appt = Appointment(
            caregiver_user_id=int(request.form["caregiver_user_id"]),
            member_user_id=int(request.form["member_user_id"]),
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            work_hours=int(request.form.get("work_hours") or 0),
            status=request.form.get("status"),
        )
        db.add(appt)
        db.commit()
        return redirect(url_for("list_appointments"))

    caregivers = db.query(Caregiver).all()
    members = db.query(Member).all()
    return render_template(
        "appointment_form.html",
        appointment=None,
        caregivers=caregivers,
        members=members,
        action="create",
    )


@app.route("/appointments/<int:appointment_id>/edit", methods=["GET", "POST"])
def edit_appointment(appointment_id):
    db = next(get_db())
    appt = db.query(Appointment).get(appointment_id)
    if not appt:
        return "Appointment not found", 404

    if request.method == "POST":
        date_str = request.form.get("appointment_date")
        time_str = request.form.get("appointment_time")

        appt.caregiver_user_id = int(request.form["caregiver_user_id"])
        appt.member_user_id = int(request.form["member_user_id"])
        appt.appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        appt.appointment_time = datetime.strptime(time_str, "%H:%M").time() if time_str else None
        appt.work_hours = int(request.form.get("work_hours") or 0)
        appt.status = request.form.get("status")
        db.commit()
        return redirect(url_for("list_appointments"))

    caregivers = db.query(Caregiver).all()
    members = db.query(Member).all()
    return render_template(
        "appointment_form.html",
        appointment=appt,
        caregivers=caregivers,
        members=members,
        action="edit",
    )


@app.route("/appointments/<int:appointment_id>/delete", methods=["POST"])
def delete_appointment(appointment_id):
    db = next(get_db())
    appt = db.query(Appointment).get(appointment_id)
    if not appt:
        return "Appointment not found", 404
    db.delete(appt)
    db.commit()
    return redirect(url_for("list_appointments"))



if __name__ == "__main__":
    app.run(debug=True)
