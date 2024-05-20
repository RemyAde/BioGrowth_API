from tortoise import Model, fields


class Address(Model):
    id = fields.IntField(pk=True, index=True)
    street_address = fields.CharField(max_length=200, null=True)
    city = fields.CharField(max_length=20, null=True)
    state = fields.CharField(max_length=20, null=True)
    country = fields.CharField(max_length=20, null=True)

    class Meta:
        table ="address"