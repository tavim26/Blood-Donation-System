from flask import request, render_template, redirect, url_for, session

from models.blood_stock import BloodStock
from models.donation import Donation
from models.report import Report
from models.schedule import Schedule
from models.user import User, db
from models.donor import Donor
from models.assistant import Assistant

def create_assistant_controllers(app):


    @app.route('/assistant_dashboard')
    def assistant_dashboard():
        assistant_id = session.get('user_id')
        assistant = User.query.get(assistant_id)

        donors = Donor.query.all()
        schedules = Schedule.query.all()
        donations = Donation.query.filter_by(AssistantID=assistant_id).all()
        blood_stocks = BloodStock.query.all()
        reports = Report.query.filter_by(AssistantID=assistant_id).all()


        return render_template(

            'assistant/assistant_dashboard.html',
            assistant=assistant,
            donations=donations,
            schedules=schedules,
            blood_stocks=blood_stocks,
            reports=reports,
            donors=donors

        )


    # Ruta pentru crearea unui Assistant
    @app.route('/create_assistant', methods=['POST'])
    def create_assistant():
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        cnp = request.form.get('cnp')

        # Creăm un utilizator nou
        new_user = User(first_name, last_name, email, password, cnp, 'assistant')
        db.session.add(new_user)
        db.session.commit()

        # Creăm un assistant
        assistant_id = new_user.UserID
        assistant = Assistant(assistant_id=assistant_id)
        db.session.add(assistant)
        db.session.commit()

        # Redirect către pagina de login
        return redirect(url_for('login'))
