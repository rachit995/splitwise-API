
import json
from flask import Blueprint, request, jsonify
from application.models.transaction import Transaction
import traceback

from marshmallow import Schema, fields, ValidationError

transaction_bp = Blueprint(
    'transaction',
    __name__,
    url_prefix='/api/v1/transaction'
)


@transaction_bp.route('/', methods=['GET'])
def list_transaction():
    try:
        all_transactions = list(
            map(lambda x: x.deserialize(), Transaction.objects.all()))
        return jsonify(
            isError=False,
            data=all_transactions
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500


@transaction_bp.route('/<string:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    try:
        transaction = Transaction.objects(id__exact=transaction_id).first()
        return jsonify(
            isError=False,
            data=transaction.deserialize()
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500
