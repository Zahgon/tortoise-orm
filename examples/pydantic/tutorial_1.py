
from tortoise import Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Tournament(Model):

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)


Tournament_Pydantic = pydantic_model_creator(Tournament)
print(Tournament_Pydantic.schema_json(indent=4))


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    tournament = await Tournament.create(name="New Tournament")
    tourpy = await Tournament_Pydantic.from_tortoise_orm(tournament)

    print(tourpy.model_dump())
    print(tourpy.model_dump_json(indent=4))


if __name__ == "__main__":
    run_async(run())
