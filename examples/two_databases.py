
from tortoise import Tortoise, connections, fields, run_async
from tortoise.exceptions import OperationalError
from tortoise.models import Model


class Tournament(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()

    def __str__(self):
        return self.name

    class Meta:
        app = "tournaments"


class Event(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    tournament_id = fields.IntField()
    participants: fields.ManyToManyRelation["Team"] = fields.ManyToManyField(
        "events.Team", related_name="events", through="event_team"
    )

    def __str__(self):
        return self.name

    class Meta:
        app = "events"


class Team(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()

    event_team: fields.ManyToManyRelation[Event]

    def __str__(self):
        return self.name

    class Meta:
        app = "events"


async def run():
    await Tortoise.init(
        {
            "connections": {
                "first": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": "example.sqlite3"},
                },
                "second": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": "example1.sqlite3"},
                },
            },
            "apps": {
                "tournaments": {"models": ["__main__"], "default_connection": "first"},
                "events": {"models": ["__main__"], "default_connection": "second"},
            },
        }
    )
    await Tortoise.generate_schemas()
    client = connections.get("first")
    second_client = connections.get("second")

    tournament = await Tournament.create(name="Tournament")
    await Event(name="Event", tournament_id=tournament.id).save()

    try:
        await client.execute_query('SELECT * FROM "event"')
    except OperationalError:
        print("Expected it to fail")
    results = await second_client.execute_query('SELECT * FROM "event"')
    print(results)


if __name__ == "__main__":
    run_async(run())
