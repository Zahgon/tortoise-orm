from tortoise import fields, migrations
from tortoise.expressions import F
from tortoise.migrations import operations as ops


async def populate_post_summary(apps, schema_editor) -> None:
    pass


async def reset_post_summary(apps, schema_editor) -> None:
    pass


class Migration(migrations.Migration):
    dependencies = [("blog", "0012_auto_20260124_1651")]

    initial = False

    operations = [
        ops.AddField(
            model_name="Post",
            name="summary",
            field=fields.TextField(null=True, unique=False),
        ),
        ops.RunPython(
            code=populate_post_summary,
            reverse_code=reset_post_summary,
        ),
    ]
