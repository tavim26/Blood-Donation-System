from flask import request, render_template, redirect, url_for
from models.user import User, db
from models.donor import Donor

def create_donor_controllers(app):


    # Ruta pentru crearea unui Donor
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
