
from __future__ import annotations

from tortoise import fields, models



class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=120, unique=True)

    class Meta:
        table = "category"
        schema = "catalog"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200)
    sku = fields.CharField(max_length=40, unique=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2)

    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        "shop.Category", related_name="products"
    )

    suppliers: fields.ManyToManyRelation[Supplier] = fields.ManyToManyField(
        "shop.Supplier",
        related_name="products",
        through="product_supplier",
    )

    class Meta:
        table = "product"
        schema = "catalog"

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"




class Supplier(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=200)
    contact_email = fields.CharField(max_length=254, null=True)

    class Meta:
        table = "supplier"
        schema = "warehouse"

    def __str__(self) -> str:
        return self.name


class Inventory(models.Model):
    id = fields.IntField(pk=True)
    quantity = fields.IntField(default=0)

    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
        "shop.Product", related_name="stock_entries"
    )

    supplier: fields.ForeignKeyRelation[Supplier] = fields.ForeignKeyField(
        "shop.Supplier", related_name="stock_entries"
    )

    class Meta:
        table = "inventory"
        schema = "warehouse"

    def __str__(self) -> str:
        return f"Inventory #{self.id} (qty={self.quantity})"
