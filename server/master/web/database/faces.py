from flask import Blueprint, jsonify, request
from database.database_manager import db
from database.models import Face
import database.queries as queries


face_api = Blueprint("face_api", __name__)


@face_api.route("/face", methods=["POST"])
def post():
    """
    Create a new face record.

    Returns:
        JSON response with the newly created face object or an error message if the data is invalid.
    """
    data = request.json
    user = data['user_id']
    face = data['face']

    # Create a new face object
    new_face = Face(
        user_id=user,
        face=face
    )


    # Add the new face to the database
    db.session.add(new_face)
    db.session.commit()

    return new_face.as_json(), 201

@face_api.route("/face/all", methods=["GET"])
def get_all():
    """
    Get a list of all faces.

    Returns:
        JSON response with a list of all face objects.
    """
    faces = Face.query.all()
    return [face.as_json() for face in faces]

@face_api.route("/face/del", methods=["DELETE"])
def del_all():
    faces = Face.query.all()
    for i in faces:
        db.session.delete(i)
        db.session.commit()
        return jsonify({'message': 'Scooter deleted successfully'})