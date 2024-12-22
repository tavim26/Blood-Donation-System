from flask import request, render_template, redirect, url_for, session, flash
from models.authentication import Authentication
from models.user import User, db
from extensions import bcrypt
from flask import jsonify

def create_user_controllers(app):

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(Email=email).first()

            # Validare credențiale
            if user and bcrypt.check_password_hash(user.Password, password):
                session['user_id'] = user.UserID
                session['role'] = user.Role

                auth = Authentication.query.filter_by(UserID=user.UserID).first()
                if not auth:
                    auth = Authentication(user_id=user.UserID)
                    db.session.add(auth)

                auth.token = True
                db.session.commit()

                if session['role'] == 'admin':
                    return jsonify({'success': True, 'redirect_url': url_for('admin_dashboard', id=user.UserID)})
                elif session['role'] == 'assistant':
                    return jsonify({'success': True, 'redirect_url': url_for('assistant_dashboard', id=user.UserID)})
                elif session['role'] == 'donor':
                    return jsonify({'success': True, 'redirect_url': url_for('donor_dashboard', id=user.UserID)})
            else:
                return jsonify({'success': False, 'message': 'Invalid email or password'}), 400

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
