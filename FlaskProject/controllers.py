from flask import request, render_template, redirect, url_for
from models import User, db, Admin, Assistant, Donor

def create_controllers(app):
    # Ruta pentru pagina de start
    @app.route('/')
    def index():
        return render_template('index.html')

    # Ruta pentru înscrierea Donor
    @app.route('/donor_signup', methods=['GET'])
    def donor_signup():
        return render_template('donor_signup.html')

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

    # Ruta pentru înscrierea Assistant
    @app.route('/assistant_signup', methods=['GET'])
    def assistant_signup():
        return render_template('assistant_signup.html')

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

        # Redirect către pagina de login
        return redirect(url_for('login'))

    # Ruta pentru înscrierea Admin
    @app.route('/admin_signup', methods=['GET'])
    def admin_signup():
        return render_template('admin_signup.html')

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

        # Redirect către pagina de login
        return redirect(url_for('login'))

    # Ruta pentru pagina de login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            # Căutăm utilizatorul după email
            user = User.query.filter_by(email=email).first()

            if user and user.password == password:
                return "Login successful!"  # Poți redirecționa aici către dashboard-ul utilizatorului
            return "Invalid credentials, please try again."

        return render_template('login.html')
