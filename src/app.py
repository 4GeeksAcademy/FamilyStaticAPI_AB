"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
from members import FamilyMember
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

john = FamilyMember(123, "John", jackson_family.last_name, 33, [7, 13, 22])
jackson_family.add_member(john)

jane = FamilyMember(jackson_family._generateId(), "Jane", jackson_family.last_name, 35, [10, 14, 3])
jackson_family.add_member(jane)

jimmy = FamilyMember(jackson_family._generateId(), "Jimmy", jackson_family.last_name, 5, [1])
jackson_family.add_member(jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    try:
        # this is how you can use the Family datastructure by calling its methods
        members = jackson_family.get_all_members()
        memAsJson = [e.toJson() for e in members]
        
        response_body = {
            "family": memAsJson
        }
        return jsonify(response_body), 200
    except:
        return "Internal Server Error", 500
    pass

@app.route('/member/<memberId>', methods=['GET'])
def get_single_member(memberId):
    try:
        # this is how you can use the Family datastructure by calling its methods
        member = jackson_family.get_member(memberId)

        if member is None:
            return "No family member with that ID", 400,

        response_body = member.toJson() 
        return jsonify(response_body), 200
    except:
        return "Internal Server Error", 500

@app.route('/member', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        print(data)
        if  'first_name' not in data or type(data.get("first_name")) != str:
            return "first_name is required and must be a String", 400
        if 'age' not in data or not data.get('age').isnumeric() or int(data.get('age')) < 0:
            return "age is required and must be a number greater than 0", 400
        if 'lucky_numbers' not in data:
            return "lucky_numbers must be an array and only numeric values", 400
        if not all(type(i) == int for i in data.get("lucky_numbers")):
            return "lucky_numbers must be an array and only numeric values", 400

        

        first_name = data.get("first_name")
        last_name = jackson_family.last_name
        age = data.get("age")
        lucky_numbers = data.get('lucky_numbers')
        memberId = 0

        if 'id' not in data:
            memberId = jackson_family._generateId()
        else:
            memberId = data.get("id")
    
        mem = FamilyMember(memberId, first_name, last_name, age, lucky_numbers)
        jackson_family.add_member(mem)
        return '',200
    except Exception as ex:
        print(ex)
        return "Internal Server Error", 500

@app.route('/member/<memberId>', methods=['DELETE'])
def delete_single_member(memberId):
    try:
        result = jackson_family.delete_member(memberId)
        return jsonify({'done': result}), 200
    except Exception as ex:
        print(ex)        
        return "Internal Server Error", 500
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
