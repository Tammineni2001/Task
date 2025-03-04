from flask import Blueprint, request, jsonify
from models import engine, session, Base
from models import User, DatasetAccess
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text


main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not 'USER_NAME' in data or not 'PASSWORD' in data or not 'ROLE_ID' in data:
        return jsonify({"message": "Invalid input"}), 400

    try:
        session.execute(
            text("""
            INSERT INTO "UTIL"."DATABBUDDY_USERS" (USER_NAME, PASSWORD, ROLE_ID)
            VALUES (:user_name, :password, :role_id)
            """),
            {'user_name': data['USER_NAME'], 'password': data['PASSWORD'], 'role_id': data['ROLE_ID']}
        )
        session.commit()
        return jsonify({"message": "User added successfully"}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"message": "User already exists"}), 409
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500


@main_blueprint.route('/add_dataset_access', methods=['POST'])
def add_dataset_access():
    data = request.get_json()
    if not data or not 'ROLE_ID' in data or not 'ROLE_NAME' in data or not 'DATASET_ACCESS' in data:
        return jsonify({"message": "Invalid input"}), 400

    try:
        session.execute(
            text("""
            INSERT INTO "UTIL"."USER_ROLES" (ROLE_ID, ROLE_NAME, DATASET_ACCESS)
            VALUES (:role_id, :role_name, :dataset_access)
            """),
            {'role_id': data['ROLE_ID'], 'role_name': data['ROLE_NAME'], 'dataset_access': data['DATASET_ACCESS']}
        )
        session.commit()
        return jsonify({"message": "Dataset access added successfully"}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"message": "Role already exists"}), 409
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500


@main_blueprint.route('/user_roles', methods=['GET'])
def get_user_roles():
    try:
        
        result = session.execute(text('SELECT * FROM "UTIL"."USER_ROLES"'))
        users = result.fetchall()
        user_list = [{"USER_NAME": row[0], "ROLE_ID": row[1]} for row in users]
        session.commit()  
        return jsonify(user_list), 200
    except Exception as e:
        session.rollback() 
        return jsonify({"message": str(e)}), 500
        
       
        
@main_blueprint.route('/update_role/<string:username>', methods=['PUT'])
def update_role(username):
    data = request.get_json()
    if not data or not 'ROLE_ID' in data:
        return jsonify({"message": "Invalid input"}), 400

    try:
        result = session.execute(
            text("""
            UPDATE "UTIL"."DATABBUDDY_USERS"
            SET ROLE_ID = :role_id
            WHERE USER_NAME = :username
            """),
            {'role_id': data['ROLE_ID'], 'username': username}
        )
        
        if result.rowcount > 0:
            session.commit()
            return jsonify({"message": "Role updated successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500
