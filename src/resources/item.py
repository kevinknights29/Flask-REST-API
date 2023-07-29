from __future__ import annotations

import uuid

from flask.views import MethodView
from flask_smorest import abort
from flask_smorest import Blueprint

from src.db import db
from src.schema import schema


blp = Blueprint("item", __name__, url_prefix="/item", description="Item operations")


@blp.route("")
class ItemList(MethodView):
    @blp.response(200, schema=schema.ItemSchema(many=True))
    def get(self):
        return db.items.values()

    @blp.arguments(schema=schema.ItemSchema)
    @blp.response(201, schema=schema.ItemSchema)
    def post(self, item_data):
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
        return item


@blp.route("/<string:item_id>")
class Item(MethodView):
    @blp.response(200, schema=schema.ItemSchema)
    def get(self, item_id):
        if item_id in db.items:
            return db.items[item_id]

        abort(404, message="Bad request. Item not found")

    @blp.arguments(schema=schema.ItemUpdateSchema)
    @blp.response(200, schema=schema.ItemSchema)
    def put(self, item_data, item_id):
        if item_id in db.items:
            item = {"id": item_id, **item_data}
            db.items[item_id] = item
            return item

        abort(404, message="Bad request. Item not found")

    def delete(self, item_id):
        if item_id in db.items:
            del db.items[item_id]
            return {"message": "item deleted"}, 200

        abort(404, message="Bad request. Item not found")
