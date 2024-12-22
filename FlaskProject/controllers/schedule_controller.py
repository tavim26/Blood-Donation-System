from flask import request, redirect, render_template, url_for, flash, session, jsonify
from extensions import db
from models.notification import Notification
from models.schedule import Schedule
from models.donor import Donor
from models.eligibility_form import EligibilityForm
from datetime import datetime


def create_schedule_controller(app):
    @app.route("/create/schedule/<int:id>", methods=["GET", "POST"])
    def create_schedule(id: int):
        donor = Donor.query.get_or_404(id)

        if request.method == "POST":
            try:
                appointment_date_str = request.form['appointment_date']
                form_id = int(request.form['form_id'])
                status = request.form.get('status', 'pending')  # Status-ul implicit este 'pending'

                appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%dT%H:%M")

                new_schedule = Schedule(
                    DonorID=id,
                    FormID=form_id,
                    AppointmentDate=appointment_date,
                    Status=status
                )

                db.session.add(new_schedule)
                db.session.commit()

                # Crearea notificării pentru donator
                notification_message = f"You have scheduled a blood donation on {appointment_date.strftime('%Y-%m-%d %H:%M')}."

                new_notification = Notification(
                    DonorID=id,
                    NotificationType='Appointment',
                    Message=notification_message
                )

                db.session.add(new_notification)
                db.session.commit()

                return jsonify({'success': True, 'message': 'Schedule created successfully!',
                                'redirect_url': url_for('donor_dashboard', id=session.get('user_id'))}), 200

            except Exception as e:
                print(str(e))
                db.session.rollback()
                return jsonify(
                    {'success': False, 'message': f'An error occurred while creating the schedule: {str(e)}'}), 500

        else:
            eligibility_forms = EligibilityForm.query.filter_by(DonorID=id).all()

            return render_template('donor/schedule_create.html', donor=donor, eligibility_forms=eligibility_forms)

    from models.notification import Notification




    @app.route("/confirm/schedule/<int:schedule_id>")
    def confirm_schedule(schedule_id: int):
        schedule = Schedule.query.get_or_404(schedule_id)
        donor_id = schedule.DonorID  # Obține DonorID din relația Schedule

        try:
            schedule.Status = 'confirmed'
            db.session.commit()

            # Adaugă notificare pentru donator
            notification = Notification(
                DonorID=donor_id,
                NotificationType="Schedule Confirmation",
                Message=f"Your schedule on {schedule.AppointmentDate.strftime('%Y-%m-%d %H:%M')} has been confirmed."
            )
            db.session.add(notification)
            db.session.commit()

            flash('Schedule confirmed successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('assistant_dashboard', id=session.get('user_id')))



    @app.route("/cancel/schedule/<int:schedule_id>")
    def cancel_schedule(schedule_id: int):
        schedule = Schedule.query.get_or_404(schedule_id)
        donor_id = schedule.DonorID  # Obține DonorID din relația Schedule

        try:
            schedule.Status = 'canceled'
            db.session.commit()

            # Adaugă notificare pentru donator
            notification = Notification(
                DonorID=donor_id,
                NotificationType="Schedule Cancellation",
                Message=f"Your schedule on {schedule.AppointmentDate.strftime('%Y-%m-%d %H:%M')} has been canceled."
            )
            db.session.add(notification)
            db.session.commit()

            flash('Schedule canceled successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('assistant_dashboard', id=session.get('user_id')))



    @app.route("/delete/schedule/<int:schedule_id>")
    def delete_schedule(schedule_id: int):
        schedule = Schedule.query.get_or_404(schedule_id)

        try:
            db.session.delete(schedule)
            db.session.commit()
            flash('Schedule deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

        return redirect(url_for('donor_dashboard', id=session.get('user_id')))




    @app.route("/update/schedule/<int:schedule_id>", methods=["GET", "POST"])
    def update_schedule(schedule_id: int):
        schedule = Schedule.query.get_or_404(schedule_id)

        if request.method == "POST":
            try:
                appointment_date_str = request.form['appointment_date']
                form_id = int(request.form['form_id'])

                appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%dT%H:%M")

                schedule.AppointmentDate = appointment_date
                schedule.FormID = form_id

                db.session.commit()

                return jsonify({'success': True, 'message': 'Schedule updated successfully!',
                                'redirect_url': url_for('donor_dashboard', id=session.get('user_id'))}), 200

            except Exception as e:
                print(str(e))
                db.session.rollback()
                return jsonify(
                    {'success': False, 'message': f'An error occurred while updating the schedule: {str(e)}'}), 500

        else:
            eligibility_forms = EligibilityForm.query.filter_by(DonorID=schedule.DonorID).all()

            return render_template('donor/schedule_update.html', schedule=schedule, eligibility_forms=eligibility_forms)
