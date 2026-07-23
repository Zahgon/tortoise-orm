import logging

from aiohttp import web
from models import Users

from tortoise.contrib.aiohttp import register_tortoise

logging.basicConfig(level=logging.DEBUG)


async def list_all(request):
    pass


async def add_user(request):
    pass


app = web.Application()
app.add_routes([web.get("/", list_all), web.post("/user", add_user)])
register_tortoise(
    app, db_url="sqlite://:memory:", modules={"models": ["models"]}, generate_schemas=True
)


if __name__ == "__main__":
    web.run_app(app, port=5000)
