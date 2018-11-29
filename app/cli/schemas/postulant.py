from marshmallow import Schema, fields

class PostulantRegRapRequestSchema(Schema):
    txtName	= fields.Str(required=True)
    txtFirstLastName = fields.Str(required=True)
    txtSecondLastName = fields.Str(required=True)
    txtEmail = fields.Str(required=True)
    pswd = fields.Str(required=True)
    txtJob = fields.Str(required=True)
    selLocation = fields.Str(required=True)
