from flask import request, render_template, redirect, url_for, session, flash

from models.authentication import Authentication
from models.user import User, db


def create_user_controllers(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(Email=email).first()

            if user and user.Password == password:
                session['user_id'] = user.UserID
                session['role'] = user.Role


                auth = Authentication.query.filter_by(UserID=user.UserID).first()
                if auth:
                    auth.token = True
                db.session.commit()

                if session['role'] == 'admin':
                    return redirect(url_for('admin_dashboard', id=user.UserID))
                elif session['role'] == 'assistant':
                    return redirect(url_for('assistant_dashboard', id=user.UserID))
                elif session['role'] == 'donor':
                    return redirect(url_for('donor_dashboard', id=user.UserID))
            else:
                flash('Invalid credentials, please try again.', 'danger')

        return render_template('login.html')

    @app.route('/logout/<int:id>')
    def logout(id: int):
        if 'user_id' in session and session['user_id'] == id:
            user = User.query.get(id)
            if user:
                auth = Authentication.query.filter_by(UserID=user.UserID).first()
                if auth:
                    auth.token = False
                    db.session.commit()

            session.clear()

        return redirect(url_for('login'))




