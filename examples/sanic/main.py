import logging

from models import Users
from sanic import Sanic, response

from tortoise.contrib.sanic import register_tortoise

logging.basicConfig(level=logging.DEBUG)

app = Sanic(__name__)


@app.route("/")
async def list_all(request):
    pass


@app.post("/user")
async def add_user(request):
    pass


register_tortoise(
    app, db_url="sqlite://db.sqlite3", modules={"models": ["models"]}, generate_schemas=True
)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
