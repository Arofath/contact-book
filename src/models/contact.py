from pydantic import BaseModel, Field, EmailStr, HttpUrl

class ContactRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, examples=['John Doe'])
    phone: str = Field(..., max_length=15, examples=['01234567890'])
    email : EmailStr | None = Field(None, examples=['johndoe@gmail.com'])
    telegram : HttpUrl | None = Field(None, examples=['https://t.me/johndoe'])
    facebook : HttpUrl | None = Field(None, examples=['https://www.facebook.com/johndoe'])
    
class ContactResponse(ContactRequest):
    id: str
    name: str
    phone: str
    avatar: str | None
    email : str | None
    telegram : str | None
    facebook : str | None
    
def contact_response(contact: dict):
    return ContactResponse(
        id=str(contact['_id']),
        name=contact['name'],
        phone=contact['phone'],
        avatar=contact['avatar'],
        email=contact['email'],
        telegram=contact['telegram'],
        facebook=contact['facebook']
    )