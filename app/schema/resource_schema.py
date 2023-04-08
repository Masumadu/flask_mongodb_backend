from marshmallow import Schema, fields


class ResourceSchema(Schema):
    id = fields.String()
    title = fields.String()
    content = fields.String()
    created = fields.DateTime()
    modified = fields.DateTime()

    class Meta:
        ordered = True


class CreateResourceSchema(ResourceSchema):
    title = fields.String(required=True)
    content = fields.String(required=True)

    class Meta:
        fields = ["title", "content"]


class UpdateResourceSchema(ResourceSchema):
    title = fields.String()
    content = fields.String()

    class Meta:
        fields = ["title", "content"]


class ResourceRequestArgumentSchema(Schema):
    page = fields.Integer()
    per_page = fields.Integer()


class TokenSchema(Schema):
    access_token = fields.String()
    refresh_token = fields.String()


class RefreshTokenSchema(Schema):
    refresh_token = fields.String()
