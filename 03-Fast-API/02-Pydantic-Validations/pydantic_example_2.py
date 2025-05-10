from pydantic import BaseModel, EmailStr


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr
    addresses: list[Address]


user_data = {
    "id": 1,
    "name": "Umar Farooq",
    "email": "umarofficial0121@gmail.com",
    "addresses": [
        {"street": "123 Main Street", "city": "Karachi", "zip_code": "12012"},
        {"street": "456 Oak Ave", "city": "Lahore", "zip_code": "12123"},
    ],
}

user = UserWithAddress.model_validate(user_data)
print(user.model_dump())
