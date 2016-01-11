from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry

app = Flask(__name__)

# app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nasa'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Nasa(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    rast = db.Column(db.String(80), unique=True)
    forecast_date = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def hello_world():
    return 'NASA rainfall data'

@app.route('/start_date=<start_date>&end_date=<end_date>&location=<location>')
def return_json(start_date, end_date, location):
    return 'Start date = {} \n End date = {} \n Location = {}'.format(start_date, end_date, location)

@app.errorhandler(404)
def not_found(error):
    return "Page not found"

if __name__ == '__main__':
    app.run(debug=True)



# from app import views