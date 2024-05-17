from marshmallow import Schema, fields, validate

class RegisterRequestSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    is_organization = fields.Bool(required=True, default=False)

class LoginRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
class OrganizationSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=80))
    description = fields.Str(required=True, validate=validate.Length(max=255))
    website = fields.Str(validate=validate.Length(max=255))
    phone = fields.Str(validate=validate.Length(max=20))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    logo = fields.Str(validate=validate.Length(max=255))
    created_by = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)



