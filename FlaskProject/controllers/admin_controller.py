from flask import request, render_template, redirect, url_for, session, flash

from models.authentication import Authentication
from models.blood_stock import BloodStock
from models.report import Report
from models.schedule import Schedule
from models.user import User
from extensions import db
from models.assistant import Assistant
from models.activity_log import ActivityLog
from models.donation import Donation
from models.donor import Donor
from models.admin import Admin


def create_admin_controllers(app):
    @app.route('/admin_dashboard/<int:id>')
    def admin_dashboard(id: int):
        admin = User.query.get(id)
        if not admin:
            flash('Admin user not found.', 'error')
            return redirect(url_for('login'))

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
        donations = Donation.query.all()
        blood_stocks = BloodStock.query.all()
        reports = Report.query.all()
        schedules = Schedule.query.all()

        return render_template(
            'admin/admin_dashboard.html',
            admin=admin,
            users=users,
            activity_logs=activity_logs,
            donors=donors,
            assistants=assistants,
            donations=donations,
            blood_stocks=blood_stocks,
            reports=reports,
            schedules=schedules
        )

    @app.route('/create_admin', methods=['POST'])
    def create_admin():
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        cnp = request.form.get('cnp')

        new_user = User(first_name, last_name, email, password, cnp, 'admin')
        db.session.add(new_user)
        db.session.commit()

        admin_id = new_user.UserID
        admin = Admin(admin_id=admin_id)
        db.session.add(admin)
        db.session.commit()

        new_auth = Authentication(user_id=new_user.UserID, token=False)
        db.session.add(new_auth)
        db.session.commit()

        return redirect(url_for('login'))
