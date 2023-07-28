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


@app.get("/store/<string:store_id>")
def get_store(name):
    if name in db.stores:
        return db.stores[name], 200
    return {"message": "store not found"}, 404


@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in db.stores:
        if store["name"] == name:
            return {"items": store["items"]}
        return {"message": "store not found"}, 404
