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

    @app.route('/add/assistant', methods=['POST', 'GET'])
    def add_assistant():
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            cnp = request.form['cnp']

            # Creăm un utilizator nou
            new_user = User(first_name, last_name, email, password, cnp, 'assistant')
            db.session.add(new_user)
            db.session.commit()

            # Creăm un asistent
            assistant_id = new_user.UserID
            assistant = Assistant(assistant_id=assistant_id)

            try:
                db.session.add(assistant)
                db.session.commit()
                return redirect(url_for('admin_dashboard'))

            except Exception as e:
                return str(e)

        return render_template('admin/assistant_create.html')



    @app.route("/delete/assistant/<int:id>")
    def deleteAssistant(id: int):
        delete_assistant = Assistant.query.get_or_404(id)

        try:
            user_to_delete = User.query.get(delete_assistant.UserID)
            db.session.delete(user_to_delete)
            db.session.delete(delete_assistant)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            return str(e)

    @app.route("/update/assistant/<int:id>", methods=['GET', 'POST'])
    def updateAssistant(id: int):

        edit_assistant = Assistant.query.get_or_404(id)
        edit_user = User.query.get_or_404(edit_assistant.UserID)

        if request.method == "POST":

            edit_user.FirstName = request.form['first_name']
            edit_user.LastName = request.form['last_name']
            edit_user.Email = request.form['email']
            edit_user.Password = request.form['password']
            edit_user.CNP = request.form['cnp']

            try:
                db.session.commit()
                return redirect(url_for('admin_dashboard'))
            except Exception as e:
                return str(e)
        else:
            return render_template('admin/assistant_update.html', assistant=edit_assistant, user=edit_user)


    
