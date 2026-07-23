
from tortoise import Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model


class Tournament(Model):

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    events: fields.ReverseRelation["Event"]

    def name_length(self) -> int:
        pass

    def events_num(self) -> int:
        pass

    class PydanticMeta:
        exclude = ("created_at",)
        computed = ("name_length", "events_num")


class Event(Model):

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    tournament: fields.ForeignKeyRelation[Tournament] = fields.ForeignKeyField(
        Tournament, related_name="events", description="The Tournament this happens in"
    )

    class Meta:
        ordering = ["name"]

    class PydanticMeta:
        exclude = ("created_at",)


Tortoise.init_models(["__main__"], "models")
Tournament_Pydantic = pydantic_model_creator(Tournament)


print(Tournament_Pydantic.schema_json(indent=4))


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    tournament = await Tournament.create(name="New Tournament")
    await Event.create(name="Event 1", tournament=tournament)
    await Event.create(name="Event 2", tournament=tournament)

    tourpy = await Tournament_Pydantic.from_tortoise_orm(tournament)

    print(tourpy.model_dump_json(indent=4))


if __name__ == "__main__":
    run_async(run())
