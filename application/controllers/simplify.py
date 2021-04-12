
from collections import defaultdict
from application.models.transaction import Transaction
from application.models.group import Group
from application.models.user_group import UserGroup
from application.models.user import User
import json
from flask import Blueprint, request, jsonify
from application.models.expense import Expense
from mongoengine.queryset.visitor import Q
import traceback

from marshmallow import Schema, fields, ValidationError

simplify_bp = Blueprint('simplify', __name__, url_prefix='/api/v1/simplify')


def get_simplified_trans(transactions, user_id=None):
    sd = []
    debit = []
    credit = []
    members = defaultdict(lambda: 0)
    for transaction in transactions:
        members[str(transaction.payer.id)] -= transaction.amount
        members[str(transaction.payee.id)] += transaction.amount
    for m in members:
        j = {
            "user": m,
            "amount": abs(members[m])
        }
        if members[m] > 0:
            credit.append(j)
        else:
            debit.append(j)
    sd = []
    for c in credit:
        for d in debit:
            if c["amount"] and d["amount"]:
                p = {}
                if d["amount"] > c["amount"]:
                    p["payer"] = d["user"]
                    p["amount"] = c["amount"]
                    p["payee"] = c["user"]
                    c["amount"] = 0
                    d["amount"] -= c["amount"]
                else:
                    p["payee"] = d["user"]
                    p["amount"] = d["amount"]
                    p["payer"] = c["user"]
                    c["amount"] -= d["amount"]
                    d["amount"] = 0
                if user_id is not None:
                    if p["payee"] == user_id or p["payer"] == user_id:
                        sd.append(p)
                else:
                    sd.append(p)
    return sd


@simplify_bp.route('/<string:group_id>', methods=['GET'])
def get_all_simplified_debts(group_id):
    try:
        all_transactions = Transaction.objects.all()
        sd = get_simplified_trans(transactions=all_transactions)
        return jsonify(
            isError=False,
            data=sd
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500


@ simplify_bp.route('/<string:group_id>/<string:user_id>', methods=['GET'])
def get_user_simplified_debts(group_id, user_id):
    try:
        all_transactions = Transaction.objects().all()
        sd = get_simplified_trans(
            transactions=all_transactions, user_id=user_id)
        return jsonify(
            isError=False,
            data=sd
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500
