
from tortoise import Tortoise, connections, fields, run_async
from tortoise.models import Model
from tortoise.transactions import in_transaction


class Event(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    timestamp = fields.DatetimeField(auto_now_add=True)


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    conn = connections.get("default")

    await conn.execute_query("INSERT INTO event (name) VALUES ('Foo')")

    await conn.execute_query("INSERT INTO event (name) VALUES (?)", ["Bar"])

    async with in_transaction("default") as tconn:
        await tconn.execute_query("INSERT INTO event (name) VALUES ('Moo')")

    async with in_transaction("default") as tconn:
        await tconn.execute_query("INSERT INTO event (name) VALUES ('Sheep')")
        await tconn.rollback()

    val = await conn.execute_query_dict("SELECT * FROM event")
    print(val)


if __name__ == "__main__":
    run_async(run())
