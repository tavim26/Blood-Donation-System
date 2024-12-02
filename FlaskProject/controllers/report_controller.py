from flask import request, redirect, render_template, url_for, session

from models.assistant import Assistant, db
from models.donation import Donation
from models.report import Report


def create_report_controller(app):


    @app.route('/create/report/<int:assistant_id>', methods=['GET', 'POST'])
    def create_report(assistant_id):
        # Căutăm asistentul curent
        assistant = Assistant.query.get_or_404(assistant_id)

        if request.method == 'POST':
            # Preluăm datele din formular și salvăm reportul
            donation_id = request.form.get('donation_id')
            report_type = request.form.get('report_type')
            report_data = request.form.get('report_data')

            new_report = Report(
                AssistantID=assistant_id,
                DonationID=donation_id,
                ReportType=report_type,
                ReportData=report_data
            )

            db.session.add(new_report)
            db.session.commit()

            return redirect(url_for('assistant_dashboard',id=session.get('user_id')))

        donations = Donation.query.all()  # Preluăm toate donațiile
        return render_template('assistant/report_create.html', assistant=assistant, donations=donations)
