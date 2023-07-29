from __future__ import annotations

from flask import Flask
from flask_smorest import Api

from src.resources.item import blp as item_blp
from src.resources.store import blp as store_blp


app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["OPENAPI_SWAGGER_UI_VERSION"] = "5.2.0"

api = Api(app)

api.register_blueprint(store_blp)
api.register_blueprint(item_blp)
