from flask import request, redirect, render_template
from database import db
from models.schedule import Schedule


def create_schedule_controller(app):
    @app.route("/create/schedule/<int:id>", methods=["GET", "POST"])
    def create_schedule(id: int):
        from datetime import datetime


        if request.method == "POST":
            # Preia datele din formular
            appointment_date = request.form.get("appointment_date")
            form_id = request.form.get("form_id")
            status = request.form.get("status", "pending")  # Status-ul poate fi 'pending' sau o valoare default

            # Validează datele (optional)
            if not appointment_date or not form_id:
                return redirect(request.url)

            # Convertim data într-un format datetime
            try:
                appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return redirect(request.url)

            # Creăm un nou obiect Schedule
            new_schedule = Schedule(
                DonorID=id,
                FormID=int(form_id),
                AppointmentDate=appointment_date,
                Status=status
            )

            # Adăugăm și comitem în baza de date
            try:
                db.session.add(new_schedule)
                db.session.commit()
                return redirect("/schedules")  # Redirecționează către o pagină relevantă
            except Exception as e:
                db.session.rollback()
                return redirect(request.url)

        else:
            return render_template("donor/schedule_create.html", donor_id=id)




