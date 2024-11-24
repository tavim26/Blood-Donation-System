from flask import request, redirect, render_template, url_for, flash
from database import db
from models.schedule import Schedule
from models.donor import Donor
from models.eligibility_form import EligibilityForm  # Asigură-te că importarea este corectă
from datetime import datetime


def create_schedule_controller(app):


    @app.route("/create/schedule/<int:id>", methods=["GET", "POST"])
    def create_schedule(id: int):
        donor = Donor.query.get_or_404(id)  # Obținem donor-ul sau returnăm 404 dacă nu există

        if request.method == "POST":
            try:
                # Preia datele din formular
                appointment_date_str = request.form['appointment_date']
                form_id = int(request.form['form_id'])
                status = request.form.get('status', 'pending')  # Status-ul implicit este 'pending'

                # Convertim data într-un format datetime fără secunde
                appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%dT%H:%M")

                # Creăm un nou obiect Schedule
                new_schedule = Schedule(
                    DonorID=id,
                    FormID=form_id,
                    AppointmentDate=appointment_date,
                    Status=status
                )

                # Adăugăm și comitem în baza de date
                db.session.add(new_schedule)
                db.session.commit()

                flash('Schedule created successfully!', 'success')
                return redirect(url_for('donor_dashboard'))  # Redirecționăm către dashboard-ul donor-ului

            except Exception as e:
                print(str(e))  # Este bine să afișezi eroarea pentru debug
                db.session.rollback()
                flash('An error occurred while creating the schedule.', 'error')
                return redirect(request.url)  # Asigurăm returnarea unei răspuns valide în caz de eroare

        else:
            # Obținem formularele de eligibilitate ale donor-ului
            eligibility_forms = EligibilityForm.query.filter_by(DonorID=id).all()

            return render_template('donor/schedule_create.html', donor=donor, eligibility_forms=eligibility_forms)



    @app.route("/confirm/schedule/<int:id>")
    def confirm_schedule(id):
        schedule = Schedule.query.get_or_404(id)
        try:
            schedule.Status = 'confirmed'
            db.session.commit()
            flash('Schedule confirmed successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('assistant_dashboard'))




    @app.route("/cancel/schedule/<int:id>")
    def cancel_schedule(id):
        schedule = Schedule.query.get_or_404(id)
        try:
            schedule.Status = 'canceled'
            db.session.commit()
            flash('Schedule cancelled successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('assistant_dashboard'))



    @app.route("/delete/schedule/<int:id>")
    def delete_schedule(id):
        schedule = Schedule.query.get_or_404(id)

        try:
            db.session.delete(schedule)
            db.session.commit()
            flash('Schedule deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('donor_dashboard'))
