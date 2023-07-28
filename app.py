from __future__ import annotations

import uuid

from flask import Flask
from flask import request

from src.db import db


app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(db.stores.items())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {"id": store_id, **store_data}
    db.stores[store_id] = new_store
    return new_store, 201


@app.post("/store/<string:store_id>/item")
def create_item(store_id):
    if store_id in db.stores:
        item_data = request.get_json()
        item_id = uuid.uuid4().hex
        item = {"id": item_id, **item_data}
        db.items[item_id] = item
        return item, 201
    return {"message": "store not found"}, 404


@app.get("/item")
def get_all_items():
    return {"items": list(db.items.values())}


@app.get("/store/<string:store_id>")
def get_store(store_id):
    if store_id in db.stores:
        return db.stores[store_id], 200
    return {"message": "store not found"}, 404


@app.get("/item/<string:item_id>")
def get_item(item_id):
    if item_id in db.items:
        return db.items[item_id], 200

    return {"message": "item not found"}, 404
