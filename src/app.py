"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404


@app.route('/members', methods=['POST'])
def add_member():
    member_data = request.get_json()
    if not member_data:
        return jsonify({"message": "Request body is missing"}), 400

    new_member = jackson_family.add_member(member_data)
    return jsonify(new_member), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    was_deleted = jackson_family.delete_member(member_id)
    if was_deleted:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"message": "Member not found"}), 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
