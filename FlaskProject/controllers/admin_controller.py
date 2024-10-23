from flask import request, render_template, redirect, url_for, session, flash
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

        users = User.query.all()
        activity_logs = ActivityLog.query.all()

        return render_template('admin_dashboard.html', admin=admin, users=users, activity_logs=activity_logs)
