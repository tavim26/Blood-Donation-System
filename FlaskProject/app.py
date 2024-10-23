from flask import Flask
from config import Config
from controllers.user_controller import create_user_controllers
from controllers.admin_controller import create_admin_controllers
from controllers.assistant_controller import create_assistant_controllers
from controllers.donor_controller import create_donor_controllers
from database import db
from controllers import create_controllers
from views import create_views



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

create_views(app)
create_controllers(app)
create_user_controllers(app)
create_admin_controllers(app)
create_assistant_controllers(app)
create_donor_controllers(app)

if __name__ == '__main__':
    app.run(debug=True)
