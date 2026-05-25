from fastapi import APIRouter, Body, Path, Query, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from src.models.contact import ContactRequest, ContactResponse, contact_response
from src.services.contact_service import insert_contact, find_contact, find_contacts, paginate_contacts, delete_contact, update_contact, update_avatar
from bson import ObjectId
from src.config.cloudinary import configure_cloudinary

contact_router = APIRouter()

@contact_router.post('/api/contacts', summary='Create new contact', tags=['Contacts',])
async def store(body : ContactRequest = Body()):
    oid = insert_contact(
        name=body.name,
        phone=body.phone,
        email=body.email,
        telegram=body.telegram,
        facebook=body.facebook
    )
    contact = find_contact(oid)
    return contact_response(contact)

@contact_router.delete('/api/contacts/{id}', summary='Delete contact by ID', tags=['Contacts',])
async def delete(id: str = Path(..., max_length=50, examples='64b64c7f8f1d2c3a4b5e6f70')):
    oid = ObjectId(id)
    contact = find_contact(oid)
    
    if contact is None:
        raise HTTPException(status_code=422, detail='Contact not found')
    
    delete_contact(oid)
    return JSONResponse(content={'message': 'Contact deleted successfully'})

@contact_router.put('/api/contacts/{id}', summary='Update contact by ID', tags=['Contacts'])
async def update(
    id: str = Path(..., max_length=50, example='64b7f8e2c9e77b1a2d3e4f5g'),
    body: ContactRequest = Body()
) -> ContactResponse:
    oid = ObjectId(id)
    contact = find_contact(oid)
    if contact is None:
        raise HTTPException(422, 'Contact not found')
    update_contact(oid, body.name, body.phone, body.email, body.telegram, body.facebook)
    contact = find_contact(oid)

    return contact_response(contact)

@contact_router.get('/api/contacts', summary='Get all contacts', tags=['Contacts'])
async def index(page: int = Query(1, ge=1), size: int = Query(5, ge=1), search: str = Query('', max_length=50)):
    contacts = find_contacts(page, size, search)
    items = []
    for contact in contacts:
        items.append(contact_response(contact))

    total, pages = paginate_contacts(size)
    return {
        'total': total,
        'page': pages,
        'current_page': page,
        'per_page': size,
        'items': items,
    }

@contact_router.get('/api/contacts/{id}', summary='Get contact by ID', tags=['Contacts'])
async def show(id: str = Path()) -> ContactResponse:
    oid = ObjectId(id)
    contact = find_contact(oid)
    if contact is None:
        raise HTTPException(422, 'Contact not found')
    return contact_response(contact)

@contact_router.post('/api/contacts-avatar/{id}', summary='Upload contact avatar', tags=['Contacts'])
async def upload_avatar(id: str = Path(..., max_length=50, examples='64b7f8e2c9e77b1a2d3e4f5g'), avatar: UploadFile = File(...)):
    oid = ObjectId(id)
    contact = find_contact(oid)
    extension = avatar.filename[-4:]
    
    if contact is None:
        raise HTTPException(422, 'Contact not found')
    
    if extension not in ['.png', '.jpg']:
        raise HTTPException(422, 'Avatar must be png or jpg')
    
    if avatar.size > 1_048_576: # 2MB
        raise HTTPException(422, 'Avatar must be less than 1MB')
    
    url = configure_cloudinary(avatar)
    update_avatar(url, oid)
    
    return JSONResponse(content={'message': 'Avatar uploaded successfully'})

# @contact_router.post('/api/contacts-avatar/{id}', summary='Upload contact avatar', tags=['Contacts'])
# async def upload_avatar(id: str = Path(..., max_length=50, examples='64b7f8e2c9e77b1a2d3e4f5g'), avatar: UploadFile = File(...)):
#     oid = ObjectId(id)
#     contact = find_contact(oid)
#     if contact is None:
#         raise HTTPException(422, 'Contact not found')
    
#     extension = avatar.filename[-4:]
#     stream = await avatar.read()
#     name = str(uuid4())
    
#     if extension not in ['.png', '.jpg']:
#         raise HTTPException(422, 'Avatar must be png or jpg')
    
#     if avatar.size > 1_048_576: # 2MB
#         raise HTTPException(422, 'Avatar must be less than 1MB')
    
#     path = f'upload/{name}.{extension}'
#     # type, size, make sure name is unique
#     w = open(path, 'wb')
#     w.write(stream)
#     w.close()
    
#     update_avatar(path, oid)
    
#     return JSONResponse(content={'message': 'Avatar uploaded successfully'})