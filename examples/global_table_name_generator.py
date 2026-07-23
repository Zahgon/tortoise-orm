
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


def snake_case_table_names(cls):
    pass


class UserProfile(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BlogPost(Model):
    id = fields.IntField(primary_key=True)
    title = fields.TextField()
    author: fields.ForeignKeyRelation[UserProfile] = fields.ForeignKeyField(
        UserProfile, related_name="posts"
    )

    class Meta:
        table = "custom_blog_posts"

    def __str__(self):
        return self.title


async def run():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["__main__"]},
        table_name_generator=snake_case_table_names,
    )
    await Tortoise.generate_schemas()

    print(f"UserProfile table name: {UserProfile._meta.db_table}")  # >>> user_profile
    print(f"BlogPost table name: {BlogPost._meta.db_table}")  # >>> custom_blog_posts

    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(run())
