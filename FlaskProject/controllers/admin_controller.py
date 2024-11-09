from flask import request, render_template, redirect, url_for, session, flash
from models.blood_stock import BloodStock
from models.report import Report
from models.schedule import Schedule
from models.user import User, db
from models.assistant import Assistant
from models.activity_log import ActivityLog
from models.donation import Donation
from models.donor import Donor
from models.admin import Admin

def create_admin_controllers(app):

    @app.route('/create_admin', methods=['POST'])
    def create_admin():
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        cnp = request.form.get('cnp')

        # Creăm un utilizator nou
        new_user = User(first_name, last_name, email, password, cnp, 'admin')
        db.session.add(new_user)
        db.session.commit()

        # Creăm un admin
        admin_id = new_user.UserID
        admin = Admin(admin_id=admin_id)
        db.session.add(admin)
        db.session.commit()

        return redirect(url_for('login'))

    @app.route('/admin_dashboard')
    def admin_dashboard():
        admin_id = session.get('user_id')
        admin = User.query.get(admin_id)

        # Obținem toți donatorii cu informațiile relevante
        donors = (
            db.session.query(
                Donor.DonorID,
                User.FirstName,
                User.LastName,
                User.Email,
                User.Password,
                User.CNP,
                Donor.Age,
                Donor.Gender,
                Donor.BloodGroup
            )
            .join(User, Donor.UserID == User.UserID)
            .all()
        )

        # Obținem toți asistenții cu informațiile relevante
        assistants = (
            db.session.query(
                Assistant.AssistantID,
                User.FirstName,
                User.LastName,
                User.Email,
                User.Password,
                User.CNP
            )
            .join(User, Assistant.UserID == User.UserID)
            .all()
        )

        users = User.query.all()
        activity_logs = ActivityLog.query.all()

        return render_template(
            'admin/admin_dashboard.html',
            admin=admin,
            users=users,
            activity_logs=activity_logs,
            donors=donors,
            assistants=assistants
        )



    #delete a donor
    @app.route("/delete/donor/<int:id>")
    def deleteDonor(id: int):
        delete_donor = Donor.query.get_or_404(id)

        try:
            # Obținem referința utilizatorului asociat
            user_to_delete = User.query.get(delete_donor.UserID)
            # Ștergem utilizatorul
            db.session.delete(user_to_delete)
            # Ștergem donatorul
            db.session.delete(delete_donor)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            return str(e)

    @app.route("/update/donor/<int:id>", methods=['GET', 'POST'])
    def updateDonor(id: int):
        # Căutăm Donor-ul după ID
        edit_donor = Donor.query.get_or_404(id)

        # Căutăm User-ul asociat Donor-ului
        edit_user = User.query.get_or_404(edit_donor.UserID)

        if request.method == "POST":
            # Actualizăm câmpurile din Donor
            edit_donor.Age = request.form['age']
            edit_donor.Gender = request.form['gender']
            edit_donor.BloodGroup = request.form['bloodgroup']

            # Actualizăm câmpurile din User
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
            # Dacă este GET, trimitem atât Donor cât și User în template
            return render_template('admin/donor_update.html', donor=edit_donor, user=edit_user)




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




    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))
