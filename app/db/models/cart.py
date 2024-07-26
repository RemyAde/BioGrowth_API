from tortoise import Model, fields


class Cart(Model):
    id = fields.IntField(pk=True, index=True)
    owner = fields.ForeignKeyField("models.User", related_name="carts")
    product = fields.ForeignKeyField("models.Product")
    quantity = fields.IntField(default=1)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_modified = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "cart"