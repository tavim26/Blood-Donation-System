from flask import Flask
from config import Config
from models import db  # Asigură-te că ai importat corect db din models
from views import create_views
from controllers import create_controllers

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context(): 
    db.create_all()

create_views(app)
create_controllers(app)

if __name__ == '__main__':
    app.run(debug=True)
