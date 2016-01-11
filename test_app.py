from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/tutorial'
app.config['SQLALCHEMY_ECHO'] = True #prints out sql statements
app.debug = True
db = SQLAlchemy(app)


class Name(db.Model):
    __tablename__ = "cities"
    name = db.Column(db.String(10), primary_key=True)
    # location = db.Column(db.Point)

    def __init__(self, username, email):
        self.name = name
        self.location = location

    def __repr__(self):
        return '<Name %r>' % self.name

if __name__ == '__main__':
    names = Name.query.all()