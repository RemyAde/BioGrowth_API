from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True, index=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    username = fields.CharField(max_length=20, null=False, unique=True)
    password = fields.CharField(max_length=200, null=False)
    first_name = fields.CharField(max_length=30, null=False)
    last_name = fields.CharField(max_length=30, null=False)
    phone_number = fields.CharField(max_length=20, null=False)
    is_verified = fields.BooleanField(default=False)
    role = fields.CharField(max_length=20, null=False, default="customer")
    join_date = fields.DatetimeField(auto_now_add=True)
    address_id = fields.ForeignKeyField("models.Address", related_name="user", null=True)
    profile_image = fields.CharField(max_length=200, null=True, default="profileDefault.jpg")

    class Meta:
        table = "users"