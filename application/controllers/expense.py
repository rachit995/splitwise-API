
from application.models.transaction import Transaction
from application.models.group import Group
from application.models.user_group import UserGroup
from application.models.user import User
import json
from flask import Blueprint, request, jsonify
from application.models.expense import Expense
import traceback

from marshmallow import Schema, fields, ValidationError

expense_bp = Blueprint('expense', __name__, url_prefix='/api/v1/expense')


class ExpenseSchema(Schema):
    title = fields.String(required=True)
    group = fields.String(required=True)
    amount = fields.Number(required=True)
    spender = fields.List(required=True, cls_or_instance=fields.Mapping)
    splits = fields.List(required=True, cls_or_instance=fields.Mapping)


@expense_bp.route('/', methods=['POST'])
def create_expense():
    try:
        request_data = request.json
        schema = ExpenseSchema()
        try:
            result = schema.load(request_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        total_spender_amount = 0
        total_amount = result["amount"]
        for sp in result["spender"]:
            total_spender_amount += sp["share"]
        total_splits_amount = 0
        for sp in result["splits"]:
            total_splits_amount += sp["share"]
        if total_spender_amount != total_splits_amount or total_spender_amount != total_amount or total_splits_amount != total_amount:
            return jsonify(
                isError=True,
                error="Amounts do not match"
            ), 500
        expense = Expense(
            title=result["title"],
            amount=total_amount,
            group=Group.objects(id__exact=result["group"]).first(),
            spender=json.dumps(result["spender"]),
            splits=json.dumps(result["splits"])
        )
        expense.save()
        total_spender_amount = 0
        spender = {}
        splits = {}
        for sp in result["spender"]:
            total_spender_amount += sp["share"]
            spender[sp["user_id"]] = sp["share"]
        total_splits_amount = 0
        for sp in result["splits"]:
            total_splits_amount += sp["share"]
            splits[sp["user_id"]] = sp["share"]
        transactions = []
        for spend in spender:
            if spender[spend] != 0:
                for split in splits:
                    if split != spend and splits[split] != 0 and spender[spend] != 0:
                        t = {}
                        if splits[split] > spender[spend]:
                            t["payee"] = split
                            t["amount"] = spender[spend]
                            t["payer"] = spend
                            spender[spend] = 0
                            splits[split] -= spender[spend]
                        else:
                            t["payee"] = split
                            t["amount"] = splits[split]
                            t["payer"] = spend
                            spender[spend] -= splits[split]
                            splits[split] = 0
                        transactions.append(t)
        for t in transactions:
            trans = Transaction(
                amount=t["amount"],
                payee=User.objects(id__exact=t["payee"]).first(),
                payer=User.objects(id__exact=t["payer"]).first(),
                expense=expense
            )
            trans.save()
        return jsonify(
            isError=False,
            data=result
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500


@expense_bp.route('/', methods=['GET'])
def list_expenses():
    try:
        all_expenses = list(
            map(lambda x: x.deserialize(), Expense.objects.all()))
        return jsonify(
            isError=False,
            data=all_expenses
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500


@expense_bp.route('/group/<string:group_id>', methods=['GET'])
def get_group_expense(group_id):
    try:
        group = Group.objects(id__exact=group_id).first()
        all_expenses = Expense.objects(group=group).all()
        all_expenses = list(
            map(lambda x: x.deserialize(), all_expenses))
        return jsonify(
            isError=False,
            data=all_expenses
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500


@expense_bp.route('/<string:expense_id>', methods=['GET'])
def get_expense(expense_id):
    try:
        expense = Expense.objects(id__exact=expense_id).first()
        return jsonify(
            isError=False,
            data=expense.deserialize()
        ), 200
    except Exception:
        err = traceback.format_exc()
        return jsonify(
            isError=True,
            data=err
        ), 500
