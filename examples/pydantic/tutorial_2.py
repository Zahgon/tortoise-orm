
from tortoise import Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_queryset_creator
from tortoise.models import Model


class Tournament(Model):

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]


Tournament_Pydantic_List = pydantic_queryset_creator(Tournament)
print(Tournament_Pydantic_List.schema_json(indent=4))


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    await Tournament.create(name="New Tournament")
    await Tournament.create(name="Another")
    await Tournament.create(name="Last Tournament")

    tourpy = await Tournament_Pydantic_List.from_queryset(Tournament.all())

    print(tourpy.model_dump())
    print(tourpy.model_dump_json(indent=4))


if __name__ == "__main__":
    run_async(run())
