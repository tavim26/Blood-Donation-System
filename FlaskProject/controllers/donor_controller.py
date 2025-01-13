from flask import request, render_template, redirect, url_for, flash, session, jsonify

from models.activity_log import ActivityLog
from models.authentication import Authentication
from models.donation import Donation
from models.eligibility_form import EligibilityForm
from models.notification import Notification
from models.schedule import Schedule
from models.user import User
from models.donor import Donor
from extensions import db


def create_donor_controllers(app):

    @app.route('/donor_dashboard/<int:id>')
    def donor_dashboard(id: int):
        user = User.query.get(id)

        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('login'))

        donor = Donor.query.filter_by(UserID=id).first()
        if not donor:
            flash('Donor not found.', 'error')
            return redirect(url_for('login'))

        schedules = Schedule.query.filter_by(DonorID=donor.DonorID).all()
        donations = db.session.query(Donation).join(Schedule).filter(Schedule.DonorID == donor.DonorID).all()
        eligibility_forms = EligibilityForm.query.filter_by(DonorID=donor.DonorID).all()
        notifications = Notification.query.filter_by(DonorID=donor.DonorID).all()

        return render_template(
            'donor/donor_dashboard.html',
            donor=donor,
            user=user,
            donations=donations,
            schedules=schedules,
            eligibility_forms=eligibility_forms,
            notifications=notifications,
        )

    @app.route('/create_donor', methods=['POST'])
    def create_donor():
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        cnp = request.form.get('cnp')
        blood_group = request.form.get('blood_group')
        age = request.form.get('age')
        gender = request.form.get('gender')


        existing_email = User.query.filter_by(Email=email).first()
        if existing_email:
            return jsonify({'success': False, 'message': 'Email is already in use.'}), 400


        existing_cnp = User.query.filter_by(CNP=cnp).first()
        if existing_cnp:
            return jsonify({'success': False, 'message': 'CNP is already in use.'}), 400

        try:

            new_user = User(first_name, last_name, email, password, cnp, 'donor')
            db.session.add(new_user)
            db.session.commit()

            donor_id = new_user.UserID
            donor = Donor(donor_id=donor_id, blood_group=blood_group, age=age, gender=gender)
            db.session.add(donor)
            db.session.commit()


            new_auth = Authentication(user_id=new_user.UserID, token=False)
            db.session.add(new_auth)
            db.session.commit()

            new_activity = ActivityLog(
                Action=f"Donor with email {new_user.Email} signed up.",
            )
            db.session.add(new_activity)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return jsonify({'success': False, 'message': 'An error occurred during user creation.'}), 500

        return jsonify({'success': True, 'redirect_url': url_for('login')}), 200

    @app.route('/add/donor', methods=['POST', 'GET'])
    def add_donor():
        admin_id = session.get('user_id')

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            cnp = request.form['cnp']
            blood_group = request.form['blood_group']
            age = request.form['age']
            gender = request.form['gender']

            if not all([first_name, last_name, email, password, cnp, blood_group, age, gender]):
                return jsonify({'success': False, 'message': 'Please fill all the fields.'}), 400

            try:
                new_user = User(first_name, last_name, email, password, cnp, 'donor')
                db.session.add(new_user)
                db.session.commit()

                donor_id = new_user.UserID
                donor = Donor(donor_id=donor_id, blood_group=blood_group, age=age, gender=gender)
                db.session.add(donor)
                db.session.commit()

                new_auth = Authentication(user_id=new_user.UserID, token=False)
                db.session.add(new_auth)
                db.session.commit()

                new_activity = ActivityLog(
                    Action=f"Donor with email {donor.user.Email} was added to the database.",
                )
                db.session.add(new_activity)
                db.session.commit()

                return jsonify({'success': True, 'redirect_url': url_for('admin_dashboard', id=admin_id)}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': f'Error adding donor: {str(e)}'}), 500

        return render_template('admin/donor_create.html')

    @app.route("/update/donor/<int:id>", methods=['GET', 'POST'])
    def updateDonor(id: int):
        edit_donor = Donor.query.get_or_404(id)
        edit_user = User.query.get_or_404(edit_donor.UserID)
        admin_id = session.get('user_id')

        if request.method == "POST":
            edit_donor.Age = request.form['age']
            edit_donor.Gender = request.form['gender']
            edit_donor.BloodGroup = request.form['bloodgroup']

            edit_user.FirstName = request.form['first_name']
            edit_user.LastName = request.form['last_name']
            edit_user.Email = request.form['email']
            edit_user.CNP = request.form['cnp']

            try:
                db.session.commit()

                new_activity = ActivityLog(
                    Action=f"Donor with email {edit_donor.user.Email} was updated.",
                )
                db.session.add(new_activity)
                db.session.commit()

                return jsonify({'success': True, 'redirect_url': url_for('admin_dashboard', id=admin_id)}), 200
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error updating donor: {str(e)}'}), 500
        else:
            return render_template('admin/donor_update.html', donor=edit_donor, user=edit_user)

    @app.route("/delete/donor/<int:id>")
    def deleteDonor(id: int):
        admin_id = session.get('user_id')

        delete_donor = Donor.query.get_or_404(id)

        try:

            schedules = Schedule.query.filter_by(DonorID=delete_donor.DonorID).all()
            for schedule in schedules:
                db.session.delete(schedule)


            eligibility_forms = EligibilityForm.query.filter_by(DonorID=delete_donor.DonorID).all()
            for form in eligibility_forms:
                db.session.delete(form)


            notifications = Notification.query.filter_by(DonorID=delete_donor.DonorID).all()
            for notification in notifications:
                db.session.delete(notification)


            user_to_delete = User.query.get(delete_donor.UserID)
            auth_to_delete = Authentication.query.filter_by(UserID=user_to_delete.UserID).first()

            if auth_to_delete:
                db.session.delete(auth_to_delete)

            db.session.delete(user_to_delete)
            db.session.delete(delete_donor)


            db.session.commit()

            new_activity = ActivityLog(
                Action=f"Donor with email {delete_donor.user.Email} was deleted.",
            )
            db.session.add(new_activity)
            db.session.commit()

            return redirect(url_for('admin_dashboard', id=admin_id))

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return str(e)






