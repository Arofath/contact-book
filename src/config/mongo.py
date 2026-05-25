import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def collection(collection_name: str):
    # ទាញយក Connection String តែមួយគត់
    url = os.getenv('MONGO_URL')
    
    # ដាក់លក្ខខណ្ឌការពារក្រែងលោអ្នកភ្លេចដាក់អថេរនេះ
    if not url:
        raise ValueError("សូមបញ្ចូល MONGO_URL នៅក្នុងឯកសារ .env ឬ Environment Variables")
        
    client = MongoClient(url)
    return client['contact_book_db'][collection_name]

# def collection(collection_name: str):
#     username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
#     password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
#     host = os.getenv('MONGO_HOST')
#     port = os.getenv('MONGO_PORT')
#     url = f'mongodb://{username}:{password}@{host}:{port}/'
#     client = MongoClient(url)
#     return client['contact_book_db'][collection_name]
    
    