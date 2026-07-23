
from decimal import Decimal

from tortoise import migrations
from tortoise.migrations import operations as ops

_CONCAT_SQL = {
    "postgres": "UPDATE employee SET full_name = first_name || ' ' || last_name WHERE full_name IS NULL",
    "sqlite": "UPDATE employee SET full_name = first_name || ' ' || last_name WHERE full_name IS NULL",
    "mysql": "UPDATE employee SET full_name = CONCAT(first_name, ' ', last_name) WHERE full_name IS NULL",
    "mssql": "UPDATE employee SET full_name = first_name + ' ' + last_name WHERE full_name IS NULL",
}


def populate_total_amount(apps, schema_editor):
    pass


def clear_total_amount(apps, schema_editor):
    pass


def populate_full_name(apps, schema_editor):
    pass


def clear_full_name(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("erp", "0010_add_computed_fields")]

    initial = False

    operations = [
        ops.RunPython(
            code=populate_total_amount,
            reverse_code=clear_total_amount,
        ),
        ops.RunPython(
            code=populate_full_name,
            reverse_code=clear_full_name,
        ),
    ]
