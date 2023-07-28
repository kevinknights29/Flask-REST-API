from __future__ import annotations

import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import abort
from flask_smorest import Blueprint

from src.db import db


blp = Blueprint("item", __name__, url_prefix="/item", description="Item operations")


@blp.route("")
class ItemList(MethodView):
    def get(self):
        return {"items": list(db.items.values())}

    def post(self):
        item_data = request.get_json()

        field_validation = (
            "price" in item_data and "store_id" in item_data and "name" in item_data
        )
        if field_validation is False:
            abort(
                400,
                message="Bad request. Missing required fields (price, store_id, name)",
            )

        duplicate_validation = item_data["name"] in [
            item["name"] for item in db.items.values()
        ] and item_data["store_id"] in [store["id"] for store in db.stores.values()]
        if duplicate_validation is True:
            abort(
                400,
                message="Bad request. Duplicate item name in store, item already exists.",
            )

        item_id = uuid.uuid4().hex
        item = {"id": item_id, **item_data}
        db.items[item_id] = item
        return item, 201


@blp.route("/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        if item_id in db.items:
            return db.items[item_id], 200

        abort(404, message="Bad request. Item not found")

    def put(self, item_id):
        item_data = request.get_json()

        field_validation = (
            "price" in item_data and "store_id" in item_data and "name" in item_data
        )
        if field_validation is False:
            abort(
                400,
                message="Bad request. Missing required fields (price, store_id, name)",
            )

        if item_id in db.items:
            item = {"id": item_id, **item_data}
            db.items[item_id] = item
            return {"message": "item updated"}, 200

        abort(404, message="Bad request. Item not found")

    def delete(self, item_id):
        if item_id in db.items:
            del db.items[item_id]
            return {"message": "item deleted"}, 200

        abort(404, message="Bad request. Item not found")
