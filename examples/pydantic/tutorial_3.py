
from tortoise import Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Tournament(Model):

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)


class Event(Model):

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    tournament: fields.ForeignKeyRelation[Tournament] = fields.ForeignKeyField(
        Tournament, related_name="events", description="The Tournament this happens in"
    )


Tournament_Pydantic_Early = pydantic_model_creator(Tournament)
print(Tournament_Pydantic_Early.schema_json(indent=4))


Tortoise.init_models(["__main__"], "models")


Tournament_Pydantic = pydantic_model_creator(Tournament)
print(Tournament_Pydantic.schema_json(indent=4))

Event_Pydantic = pydantic_model_creator(Event)
print(Event_Pydantic.schema_json(indent=4))


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    tournament = await Tournament.create(name="New Tournament")
    event = await Event.create(name="The Event", tournament=tournament)

    tourpy = await Tournament_Pydantic.from_tortoise_orm(tournament)

    print(tourpy.model_dump_json(indent=4))

    eventpy = await Event_Pydantic.from_tortoise_orm(event)

    print(eventpy.model_dump_json(indent=4))


if __name__ == "__main__":
    run_async(run())
