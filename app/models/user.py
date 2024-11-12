from tortoise import fields, models

# from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.CharField(pk=True, max_length=50)
    username = fields.CharField(max_length=50)
    
    class Meta:
        table = "users"


# class Operation(models.Model):
#     id = fields.CharField(pk=True, max_length=50)

#     class Meta:
#         app = "sim"
#         table = "operations"
#         indexes = [
#         ]


# class SubOperation(models.Model):
#     operation = fields.ForeignKeyField("sim.Operation", related_name="sub_operations", null=True, on_delete=fields.CASCADE)

#     class Meta:
#         app = "sim"
#         table = "sub_operations"
#         indexes = [
#             ("operation_id", "record_time"),
#         ]
