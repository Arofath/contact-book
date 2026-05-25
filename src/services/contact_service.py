from src.config.mongo import collection
import math

contact_collection = collection('contacts')

def insert_contact(name, phone, email, telegram, facebook):
    result = contact_collection.insert_one({
        'avatar': None,
        'name': name,
        'phone': phone,
        'email': email,
        'telegram': str(telegram),
        'facebook': str(facebook)
    })
    return result.inserted_id

def find_contact(oid):
    return contact_collection.find_one({'_id': oid})

def find_contacts(page, sizes, search=None):
    skip = (page - 1) * sizes
    return contact_collection.find(
        {
            'name': {'$regex': search, '$options': 'i'}
        }
    ).sort({'name': 1}).skip(skip).limit(sizes).to_list()

def paginate_contacts(size):
    total = contact_collection.count_documents({})
    page = math.ceil(total / size)
    return total, page

def delete_contact(oid):
    contact_collection.delete_one({'_id': oid})
    
def update_contact(oid, name, phone, email, telegram, facebook ):
    contact_collection.update_one(
        {'_id': oid},
        {
            '$set': {
                'name': name,
                'phone': phone,
                'email': email,
                'telegram': str(telegram),
                'facebook': str(facebook)
            }
        }
    )
    
def update_avatar(filename, oid):
    contact_collection.update_one(
        {'_id': oid},
        {
            '$set': {
                'avatar': filename
            }
        }
    )
    