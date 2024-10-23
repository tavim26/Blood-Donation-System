from flask import render_template

def create_views(app):
    @app.route('/')
    def home():
        return render_template('index.html')