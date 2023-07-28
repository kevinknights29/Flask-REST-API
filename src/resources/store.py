from __future__ import annotations

import uuid

from flask.views import MethodView
from flask_smorest import abort
from flask_smorest import Blueprint

from src.db import db
from src.schema import schema


blp = Blueprint("store", __name__, url_prefix="/store", description="Store operations")


@blp.route("")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(db.stores.values())}

    @blp.arguments(schema=schema.StoreSchema)
    def post(self, store_data):
        duplicate_validation = store_data["name"] in [
            store["name"] for store in db.stores.values()
        ]
        if duplicate_validation is True:
            abort(
                400,
                message="Bad request. Store name already exists.",
            )

        store_id = uuid.uuid4().hex
        store = {"id": store_id, **store_data}
        db.stores[store_id] = store
        return store, 201


@blp.route("/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        if store_id in db.stores:
            return db.stores[store_id], 200
        abort(404, message="Bad Request. Store not found")

    def delete(self, store_id):
        if store_id in db.stores:
            del db.stores[store_id]
            return {"message": "store deleted"}, 200

        abort(404, message="Bad request. Store not found")
