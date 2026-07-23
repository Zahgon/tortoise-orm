import asyncio
import logging
from random import choice

from models import Users, Workers
from quart import Quart, jsonify

from tortoise.contrib.quart import register_tortoise

logging.basicConfig(level=logging.DEBUG)


STATUSES = ["New", "Old", "Gone"]
app = Quart(__name__)


@app.route("/")
async def list_all():
    pass


@app.route("/user")
async def add_user():
    pass


@app.route("/worker")
async def add_worker():
    pass


register_tortoise(
    app,
    db_url="mysql://root:@127.0.0.1:3306/quart",
    modules={"models": ["models"]},
    generate_schemas=False,
)


if __name__ == "__main__":
    app.run(port=5000)
