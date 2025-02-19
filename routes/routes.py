from flask import Blueprint, request, jsonify
from models import engine, session, Base, User, DatasetAccess

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not 'USER_NAME' in data or not 'PASSWORD' in data or not 'ROLE_ID' in data:
        return jsonify({"message": "Invalid input"}), 400

    new_user = User(
        USER_NAME=data['USER_NAME'],
        PASSWORD=data['PASSWORD'],
        ROLE_ID=data['ROLE_ID']
    )
    session.add(new_user)
    session.commit()
    return jsonify({"message": "User added successfully"}), 201

@main_blueprint.route('/add_dataset_access', methods=['POST'])
def add_dataset_access():
    data = request.get_json()
    if not data or not 'ROLE_ID' in data or not 'ROLE_NAME' in data or not 'DATASET_ACCESS' in data:
        return jsonify({"message": "Invalid input"}), 400

    new_access = DatasetAccess(
        ROLE_ID=data['ROLE_ID'],
        ROLE_NAME=data['ROLE_NAME'],
        DATASET_ACCESS=data['DATASET_ACCESS']
    )
    session.add(new_access)
    session.commit()
    return jsonify({"message": "Dataset access added successfully"}), 201

@main_blueprint.route('/user_roles', methods=['GET'])
def get_user_roles():
    users = session.query(User).all()
    user_list = [{"USER_NAME": user.USER_NAME, "ROLE_ID": user.ROLE_ID} for user in users]
    return jsonify(user_list), 200

@main_blueprint.route('/update_role/<string:username>', methods=['PUT'])
def update_role(username):
    data = request.get_json()
    if not data or not 'ROLE_ID' in data:
        return jsonify({"message": "Invalid input"}), 400
    user = session.query(User).filter(User.USER_NAME == username).first()
    if user:
        user.ROLE_ID = data["ROLE_ID"]
        session.commit()
        return jsonify({"message": "Role updated successfully"}), 200
    return jsonify({"message": "User not found"}), 404
