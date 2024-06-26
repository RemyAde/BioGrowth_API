from tortoise import Model, fields


class Plan(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=20, null=False, index=True)
    monthly_price = fields.DecimalField(max_digits=12, decimal_places=2)
    annual_price = fields.DecimalField(max_digits=12, decimal_places=2)
    annual_discount = fields.DecimalField(max_digits=12, decimal_places=2)
    date_creaed = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "plan"