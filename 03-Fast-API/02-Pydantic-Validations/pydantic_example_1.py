from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None


user_data = {
    "id": 1,
    "name": "Umar Farooq",
    "email": "umarofficial0121@gmail.com",
    "age": 17,
}

user = User(**user_data)
print(user)
print(user.model_dump())

try:
    invalid_data = {"id": "Not An Integer", "name": "Umar Farooq", "email": "10"}
    user = User(**invalid_data)
except ValidationError as e:
    print(e)
