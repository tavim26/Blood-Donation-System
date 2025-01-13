from flask import request, redirect, render_template, url_for, session, flash, jsonify

from models.activity_log import ActivityLog
from models.assistant import Assistant, db
from models.donation import Donation
from models.report import Report


def create_report_controller(app):
    @app.route('/create/report/<int:assistant_id>/<int:donation_id>', methods=['GET', 'POST'])
    def create_report(assistant_id, donation_id):
        assistant = Assistant.query.get_or_404(assistant_id)
        donation = Donation.query.get_or_404(donation_id)

        if request.method == 'GET':
            return render_template('assistant/report_create.html', assistant=assistant, donation=donation)

        elif request.method == 'POST':
            report_type = request.form.get('report_type')
            report_data = request.form.get('report_data')

            if not report_type or not report_data:
                flash('All fields are required.', 'danger')
                return redirect(url_for('create_report', assistant_id=assistant_id, donation_id=donation_id))

            new_report = Report(
                AssistantID=assistant_id,
                DonationID=donation_id,
                ReportType=report_type,
                ReportData=report_data
            )

            try:
                db.session.add(new_report)
                db.session.commit()

                new_activity = ActivityLog(
                    Action=f"Assistant with email {assistant.user.email} created a report for {donation.DonationName}",
                )
                db.session.add(new_activity)
                db.session.commit()

                flash('Report created successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating report: {str(e)}', 'danger')
                return redirect(url_for('create_report', assistant_id=assistant_id, donation_id=donation_id))


            user_id = session.get('user_id')
            if user_id:

                return redirect(url_for('assistant_dashboard', id=user_id))
            else:
                flash('User session expired or not found.', 'danger')
                return redirect(url_for('login'))


    @app.route('/delete/report/<int:report_id>', methods=['GET', 'POST'])
    def delete_report(report_id):
        report = Report.query.get_or_404(report_id)

        try:
            db.session.delete(report)
            db.session.commit()

            new_activity = ActivityLog(
                Action=f"Report with id {report_id} was deleted",
            )
            db.session.add(new_activity)
            db.session.commit()

            flash('Report deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting report: {str(e)}', 'danger')

        return redirect(url_for('assistant_dashboard', id=session.get('user_id')))


