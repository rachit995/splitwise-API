
from application.models.user_group import UserGroup
from application.models.user import User
import json
from flask import Blueprint, request, jsonify
from application.models.group import Group
import traceback

from marshmallow import Schema, fields, ValidationError

group_bp = Blueprint('group', __name__, url_prefix='/api/v1/group')


class GroupSchema(Schema):
    name = fields.String(required=True)
    members = fields.List(required=True, cls_or_instance=fields.String)


@group_bp.route('/', methods=['POST'])
def create_group():
    try:
        request_data = request.json
        schema = GroupSchema()
        try:
            result = schema.load(request_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        member_ids = result['members']
        members = User.objects(id__in=member_ids)
        group = Group(
            name=result['name'],
        )
        group.save()
        for member in members:
            user_group = UserGroup(
                group=group,
                user=member
            )
            user_group.save()
        return jsonify(
            isError=False,
            data=group.deserialize()
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500


@group_bp.route('/', methods=['GET'])
def list_group():
    try:
        all_groups = list(map(lambda x: x.deserialize(), Group.objects.all()))
        return jsonify(
            isError=False,
            data=all_groups
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500


@group_bp.route('/<string:group_id>', methods=['GET'])
def get_group(group_id):
    try:
        group = Group.objects(id__exact=group_id).first()
        return jsonify(
            isError=False,
            data=group.deserialize()
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500
