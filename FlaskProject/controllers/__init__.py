from flask import render_template
from controllers.user_controller import create_user_controllers


def create_controllers(app):
    # Ruta pentru pagina de start
    @app.route('/')
    def index():
        return render_template('index.html')

        # Ruta pentru înscrierea Donor
    @app.route('/donor_signup', methods=['GET'])
    def donor_signup():
        return render_template('donor_signup.html')

        # Ruta pentru înscrierea Admin
    @app.route('/admin_signup', methods=['GET'])
    def admin_signup():
        return render_template('admin_signup.html')

    # Ruta pentru înscrierea Assistant
    @app.route('/assistant_signup', methods=['GET'])
    def assistant_signup():
        return render_template('assistant_signup.html')



