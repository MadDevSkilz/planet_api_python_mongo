from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient  # Database connector
import json  # but not the argonauts
app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return render_template("index.html")


@app.route('/api/v1/planets', methods=["GET"])
def list_planets():
    client = MongoClient("localhost", 27017)
    db = client["planetsdb"]
    planet_collection = db["planets"]
    planet_result = planet_collection.find()
    planets = []
    for planet in planet_result:
        planet["_id"] = str(planet["_id"])
        planets.append(planet)
    return jsonify(planets)


@app.route('/api/v1/add', methods=['POST'])
def add_planet():
    status_code = 200
    message = "OK - Planet Added"
    result = {}
    try:
        planet_collection = get_connection()
        form_object = process_request(request=request)
        inserted = planet_collection.insert_one(form_object)
        result['inserted_id'] = str(inserted.inserted_id)
    except:
        status_code = 500
        message = "ERROR"

    result["message"] = message
    return jsonify(result), status_code


@app.route('/api/v1/update', methods=['PUT'])
def update_planet():
    result = {}
    message = "OK - Planet Updated"
    status_code = 202  # the changes were accepted
    try:
        form_object = process_request(request=request)
        planet_id = form_object["_id"]
        planet_collection = get_connection()
        updated = planet_collection.update({"_id": planet_id}, form_object)
        result["num_documents_updated"] = updated["n"]
    except:
        status_code = 500
        message = "Error"

    result["message"] = message
    return jsonify(result), status_code


@app.route('/api/v1/delete', methods=['DELETE'])
def delete_planet():
    result = {}
    status_code = 200
    message = "I felt a great disturbance in the Force, as if millions of voices suddenly cried out in terror, " \
              "and were suddenly silenced. I fear something terrible has happened. "
    try:
        planet = process_request(request=request)
        planet_collection = get_connection()
        deleted = planet_collection.delete_one({"_id": planet['_id']})
        result["num_documents_deleted"] = deleted['n']
    except:
        status_code = 500
        result["message"] = message

    return jsonify(result), status_code


def get_connection():
    client = MongoClient("localhost", 27017)
    db = client["planetsdb"]
    planet_collection = db["planets"]
    return planet_collection


def process_request(request):
    if request.is_json:
        form_object = request.get_json()
    else:
        form_object = {"planetName": request.form["planetName"], "planetType": request.form["planetType"],
                       "mass": float(request.form["mass"]), "radius": float(request.form["radius"])}

    return form_object


if __name__ == '__main__':
    app.run()
