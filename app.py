from __future__ import annotations

import uuid

from flask import Flask
from flask import request
from flask_smorest import abort

from src.db import db


app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(db.stores.items())}


@app.post("/store")
def create_store():
    store_data = request.get_json()

    field_validation = "name" in store_data
    if field_validation is False:
        abort(400, message="Bad request. Missing required field (name)")

    duplicate_validation = store_data["name"] in [
        store["name"] for store in db.stores.values()
    ]
    if duplicate_validation is True:
        abort(400, message="Bad request. Duplicate store name, store already exists.")

    store_id = uuid.uuid4().hex
    new_store = {"id": store_id, **store_data}
    db.stores[store_id] = new_store
    return new_store, 201


@app.post("/item")
def create_item():
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


@app.get("/item")
def get_all_items():
    return {"items": list(db.items.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    if store_id in db.stores:
        return db.stores[store_id], 200
    abort(404, message="store not found")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    if item_id in db.items:
        return db.items[item_id], 200

    abort(404, message="item not found")
