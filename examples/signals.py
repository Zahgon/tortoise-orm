
from __future__ import annotations

from tortoise import BaseDBAsyncClient, Tortoise, fields, run_async
from tortoise.models import Model
from tortoise.signals import post_delete, post_save, pre_delete, pre_save


class Signal(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()

    class Meta:
        table = "signal"

    def __str__(self):
        return self.name


@pre_save(Signal)
async def signal_pre_save(sender: type[Signal], instance: Signal, using_db, update_fields) -> None:
    pass


@post_save(Signal)
async def signal_post_save(
    sender: type[Signal],
    instance: Signal,
    created: bool,
    using_db: BaseDBAsyncClient | None,
    update_fields: list[str],
) -> None:
    pass


@pre_delete(Signal)
async def signal_pre_delete(
    sender: type[Signal], instance: Signal, using_db: BaseDBAsyncClient | None
) -> None:
    pass


@post_delete(Signal)
async def signal_post_delete(
    sender: type[Signal], instance: Signal, using_db: BaseDBAsyncClient | None
) -> None:
    pass


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()
    signal = await Signal.create(name="Signal")
    signal.name = "Signal_Save"

    await signal.save(update_fields=["name"])

    await signal.delete()


if __name__ == "__main__":
    run_async(run())
