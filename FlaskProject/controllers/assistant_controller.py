from flask import request, render_template, redirect, url_for, session, flash

from models.authentication import Authentication
from models.blood_stock import BloodStock
from models.donation import Donation
from models.eligibility_form import EligibilityForm
from models.report import Report
from models.schedule import Schedule
from models.user import User
from models.donor import Donor
from models.assistant import Assistant
from extensions import db


def create_assistant_controllers(app):

    @app.route('/assistant_dashboard/<int:id>')
    def assistant_dashboard(id: int):
        user = User.query.get(id)
        assistant = Assistant.query.filter_by(UserID=id).first()

        if not user or not assistant:
            flash('Assistant not found.', 'error')
            return redirect(url_for('login'))

        donors = Donor.query.all()
        schedules = Schedule.query.all()
        donations = Donation.query.all()
        blood_stocks = BloodStock.query.all()
        reports = Report.query.filter_by(AssistantID=id).all()
        forms = EligibilityForm.query.all()

        return render_template(
            'assistant/assistant_dashboard.html',
            user=user,
            assistant=assistant,
            donors=donors,
            schedules=schedules,
            donations=donations,
            blood_stocks=blood_stocks,
            reports=reports,
            forms=forms
        )




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

        # Creăm o intrare în tabela Authentication
        new_auth = Authentication(user_id=new_user.UserID, token=False)
        db.session.add(new_auth)
        db.session.commit()

        # Redirect către pagina de login
        return redirect(url_for('login'))



    @app.route('/add/assistant', methods=['POST', 'GET'])
    def add_assistant():
        admin_id = session.get('user_id')  # Obținem admin_id din sesiune

        if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            cnp = request.form.get('cnp')

            # Verificăm dacă toate câmpurile sunt completate
            if not all([first_name, last_name, email, password, cnp]) or admin_id is None:
                flash('Please fill all the fields.', 'error')
                return redirect(url_for('add_assistant', admin_id=admin_id))

            # Creăm un utilizator și un asistent
            new_user = User(first_name, last_name, email, password, cnp, 'assistant')
            db.session.add(new_user)
            db.session.commit()

            assistant_id = new_user.UserID
            assistant = Assistant(assistant_id=assistant_id)

            try:
                db.session.add(assistant)
                db.session.commit()

                new_auth = Authentication(user_id=new_user.UserID, token=False)
                db.session.add(new_auth)
                db.session.commit()

                return redirect(url_for('admin_dashboard', id=admin_id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating assistant: {str(e)}', 'error')
                return redirect(url_for('add_assistant', admin_id=admin_id))

        if not admin_id:
            flash('Admin ID is missing.', 'error')
            return redirect(url_for('admin_dashboard'))

        return render_template('admin/assistant_create.html', admin_id=admin_id)




    @app.route("/delete/assistant/<int:id>")
    def delete_assistant(id: int):
        del_assistant = Assistant.query.get_or_404(id)

        admin_id = session.get('user_id')  # Obținem admin_id din sesiune

        try:
            user_to_delete = User.query.get(del_assistant.UserID)
            print(f"Deleting user with ID: {user_to_delete.UserID}")

            auth_to_delete = Authentication.query.filter_by(UserID=user_to_delete.UserID).first()
            if auth_to_delete:
                db.session.delete(auth_to_delete)
                print(f"Deleted authentication with ID: {auth_to_delete.AuthID}")

            db.session.delete(user_to_delete)
            db.session.delete(del_assistant)
            db.session.commit()
            print("Deleted user and assistant.")

            return redirect(url_for('admin_dashboard',id=admin_id))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return str(e)




    @app.route("/update/assistant/<int:id>", methods=['GET', 'POST'])
    def updateAssistant(id: int):

        edit_assistant = Assistant.query.get_or_404(id)
        edit_user = User.query.get_or_404(edit_assistant.UserID)

        admin_id = session.get('user_id')  # Obținem admin_id din sesiune

        if request.method == "POST":

            edit_user.FirstName = request.form['first_name']
            edit_user.LastName = request.form['last_name']
            edit_user.Email = request.form['email']
            edit_user.Password = request.form['password']
            edit_user.CNP = request.form['cnp']

            try:
                db.session.commit()
                return redirect(url_for('admin_dashboard',id=admin_id))
            except Exception as e:
                return str(e)
        else:
            return render_template('admin/assistant_update.html', assistant=edit_assistant, user=edit_user)


    
