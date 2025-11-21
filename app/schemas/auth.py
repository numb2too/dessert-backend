from apiflask import Schema
from apiflask.fields import String, Integer, Nested
from apiflask.validators import Length

class LoginInput(Schema):
    username = String(required=True, validate=Length(min=3, max=50))
    password = String(required=True, validate=Length(min=6))

class UserOutput(Schema):
    id = Integer()
    username = String()
    employee_id = Integer()
    employee_name = String()
    department = String()

class LoginOutput(Schema):
    access_token = String()
    refresh_token = String()
    user = Nested(UserOutput)

class RefreshOutput(Schema):
    access_token = String()