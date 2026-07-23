
import json

from pydantic_core import PydanticSerializationError

from tortoise import Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import NoValuesFetched
from tortoise.models import Model


class Department(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)

    employees: fields.ReverseRelation["Employee"]

    def employee_count(self) -> int:
        pass

    def employee_names(self) -> str:
        pass

    class PydanticMeta:
        computed = ("employee_count", "employee_names")


class Employee(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)

    department: fields.ForeignKeyNullableRelation[Department] = fields.ForeignKeyField(
        "models.Department", related_name="employees", null=True
    )


Tortoise.init_models(["__main__"], "models")


async def run():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()

    engineering = await Department.create(name="Engineering")
    await Employee.create(name="Alice", department=engineering)
    await Employee.create(name="Bob", department=engineering)
    await Employee.create(name="Charlie")  # no department (nullable FK)

    print("=" * 70)
    print("Section 1: Nullable FK is Optional")
    print("=" * 70)

    Employee_Pydantic = pydantic_model_creator(Employee)
    schema = Employee_Pydantic.model_json_schema()
    print(json.dumps(schema, indent=4))

    required = schema.get("required", [])
    print(f"\nRequired fields: {required}")
    print("'department' in required:", "department" in required)

    dept_props = schema.get("properties", {}).get("department", {})
    has_default_null = dept_props.get("default") is None and "default" in dept_props
    print(f"'department' has default null: {has_default_null}")

    print("\n" + "=" * 70)
    print("Section 2: Computed field with included relation")
    print("=" * 70)

    Department_Pydantic = pydantic_model_creator(Department)

    dept = await Department.get(name="Engineering")
    dept_pydantic = await Department_Pydantic.from_tortoise_orm(dept)
    print(dept_pydantic.model_dump_json(indent=4))

    print(f"\nemployee_count: {dept_pydantic.employee_count}")
    print(f"employee_names: {dept_pydantic.employee_names}")

    print("\n" + "=" * 70)
    print("Section 3: Excluded relation + manual prefetch")
    print("=" * 70)

    Department_Pydantic_NoEmployees = pydantic_model_creator(
        Department,
        name="Department_NoEmployees",
        exclude=("employees",),
    )

    dept = await Department.get(name="Engineering")
    await dept.fetch_related("employees")
    dept_pydantic = await Department_Pydantic_NoEmployees.from_tortoise_orm(dept)
    print(dept_pydantic.model_dump_json(indent=4))

    print(f"\nemployee_count: {dept_pydantic.employee_count}")
    print(f"employee_names: {dept_pydantic.employee_names}")

    print("\n" + "=" * 70)
    print("Section 4: NoValuesFetched error propagation")
    print("=" * 70)

    dept = await Department.get(name="Engineering")
    dept_pydantic = await Department_Pydantic_NoEmployees.from_tortoise_orm(dept)
    try:
        dept_pydantic.model_dump_json(indent=4)
    except (PydanticSerializationError, NoValuesFetched) as e:
        print(f"Caught error during serialization: {e}")

    print("\n" + "=" * 70)
    print("Section 5: Graceful handling pattern")
    print("=" * 70)

    class GracefulMeta:
        computed = ("employee_count",)

    Department_Pydantic_GracefulOnly = pydantic_model_creator(
        Department,
        name="Department_GracefulOnly",
        exclude=("employees",),
        meta_override=GracefulMeta,
    )

    dept = await Department.get(name="Engineering")
    dept_pydantic = await Department_Pydantic_GracefulOnly.from_tortoise_orm(dept)
    print(dept_pydantic.model_dump_json(indent=4))

    print(f"\nemployee_count (graceful, no prefetch): {dept_pydantic.employee_count}")
    print(
        "employee_names would raise NoValuesFetched in the same scenario, "
        "but employee_count handles it and returns 0."
    )


if __name__ == "__main__":
    run_async(run())
