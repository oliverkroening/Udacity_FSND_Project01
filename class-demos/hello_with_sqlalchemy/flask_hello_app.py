from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Home of Website with String "Hello World"
@app.route('/')
def index():
    # fetch name from database
    person=Person.query.first()
    return 'Hello ' + person.name



# set configuration variables
# set DB-URI
#   structure: 'dialect://username:password@host(ip-address):port/db-name'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Oll1N00sh1n@localhost:5432/example'
# set TRACK_MODIFICATIONS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# link an instance of the database to interact
db = SQLAlchemy(app)

# create class or model or table - inherited from db.Model:
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    # define repr-method for Person
    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

# create tables in database (detects models and creates tables for them, if they don't exist)
with app.app_context():
    db.create_all()

# run flask webserver via CLI: 
# > set FLASK_APP=app.py
# > (opional DEBUG-MODE to make changes while running the server)set FLASK_DEBUG=true
# > flask run 
# 
# open website: http://127.0.0.1:5000/ (localhost)

# alternative:
# always include this at the bottom of your code
if __name__ == '__main__':
   app.run(host="0.0.0.0")

# run webserver: python3 app.py
