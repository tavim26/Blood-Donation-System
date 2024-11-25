from flask import request, render_template, redirect, url_for, flash, session

from models.donation import Donation
from models.eligibility_form import EligibilityForm
from models.notification import Notification
from models.reward import Reward
from models.schedule import Schedule
from models.user import User, db
from models.donor import Donor

def create_donor_controllers(app):


    @app.route('/donor_dashboard')
    def donor_dashboard():
        user_id = session.get('user_id')
        if user_id is None:
            flash('Please log in to access the dashboard.', 'error')
            return redirect(url_for('login'))

        # Obținem utilizatorul asociat user_id
        user = User.query.get(user_id)

        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('login'))

        # Obținem donor-ul folosind user_id
        donor = Donor.query.filter_by(UserID=user_id).first()
        if not donor:
            flash('Donor not found.', 'error')
            return redirect(url_for('login'))

        # Debug pentru verificare DonorID
        print(f"DonorID: {donor.DonorID}")

        # Folosim DonorID pentru a obține informațiile donorului

        schedules = Schedule.query.filter_by(DonorID=donor.DonorID).all()
        donations = db.session.query(Donation).join(Schedule).filter(Schedule.DonorID == donor.DonorID).all()
        eligibility_forms = EligibilityForm.query.filter_by(DonorID=donor.DonorID).all()
        notifications = Notification.query.filter_by(DonorID=donor.DonorID).all()
        rewards = Reward.query.filter_by(DonorID=donor.DonorID).all()

        return render_template(
            'donor/donor_dashboard.html',
            donor=donor,
            user=user,
            donations=donations,
            schedules=schedules,
            eligibility_forms=eligibility_forms,
            notifications=notifications,
            rewards=rewards
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


        # Creăm un utilizator nou
        new_user = User(first_name, last_name, email, password, cnp, 'donor')
        db.session.add(new_user)
        db.session.commit()

        # Creăm un donor
        donor_id = new_user.UserID
        donor = Donor(donor_id=donor_id, blood_group=blood_group, age=age, gender=gender)
        db.session.add(donor)
        db.session.commit()

        # Redirect către pagina de login
        return redirect(url_for('login'))




    @app.route('/add/donor', methods=['POST','GET'])
    def add_donor():

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            cnp = request.form['cnp']
            blood_group = request.form['blood_group']
            age = request.form['age']
            gender = request.form['gender']

            # Creăm un utilizator nou
            new_user = User(first_name, last_name, email, password, cnp, 'donor')
            db.session.add(new_user)
            db.session.commit()

            # Creăm un donor
            donor_id = new_user.UserID
            donor = Donor(donor_id=donor_id, blood_group=blood_group, age=age, gender=gender)

            try:
                db.session.add(donor)
                db.session.commit()
                return redirect(url_for('admin_dashboard'))

            except Exception as e:
                return str(e)

        return render_template('admin/donor_create.html')




        # delete a donor
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








