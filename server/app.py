# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response ,jsonify
from flask_migrate import Migrate

from models import db, Earthquake



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake=Earthquake.query.filter(Earthquake.id == id).first()
    if earthquake is None:
        body ={'message':f"Earthquake {id} not found."}
        return make_response(jsonify(body), 404)
    else :
        body = {
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        }
        return make_response(jsonify(body), 200)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquake = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_list =[quake.to_dict() for quake in earthquake]
    body = {
        'count': len(quakes_list),
        'quakes': quakes_list
    }
    return make_response(jsonify(body),200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
