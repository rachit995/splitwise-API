import json
from flask import Blueprint, request, jsonify
from application.models.user import User
import traceback

from marshmallow import Schema, fields, ValidationError

user_bp = Blueprint('user', __name__, url_prefix='/api/v1/user')


class UserSchema(Schema):
    name = fields.String(required=True)


@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        request_data = request.json
        schema = UserSchema()
        try:
            result = schema.load(request_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        user = User(
            name=result['name'],
        )
        user.save()
        return jsonify(
            isError=False,
            data=user.deserialize()
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500


@user_bp.route('/', methods=['GET'])
def list_user():
    try:
        all_users = list(map(lambda x: x.deserialize(), User.objects.all()))
        return jsonify(
            isError=False,
            data=all_users
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500


@user_bp.route('/<string:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.objects(id__exact=user_id)[0]
        return jsonify(
            isError=False,
            data=user.deserialize()
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500
