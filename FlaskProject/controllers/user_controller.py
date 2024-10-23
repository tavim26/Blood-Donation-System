from flask import request, render_template, redirect, url_for, session, flash
from models.user import User, db

def create_user_controllers(app):


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            # Cautăm utilizatorul în baza de date
            user = User.query.filter_by(Email=email).first()

            # Verificăm dacă utilizatorul există și dacă parola este corectă
            if user and user.Password == password:
                # Setăm sesiunea utilizatorului
                session['user_id'] = user.UserID
                session['role'] = user.Role

                # Redirecționăm în funcție de rol
                if session['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif session['role'] == 'assistant':
                    return redirect(url_for('assistant_dashboard'))
                elif session['role'] == 'donor':
                    return redirect(url_for('donor_dashboard'))
            else:
                flash('Invalid credentials, please try again.', 'danger')

        return render_template('login.html')
