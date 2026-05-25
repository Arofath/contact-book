import cloudinary
from cloudinary.uploader import upload
from fastapi import UploadFile
import os

def configure_cloudinary(image: UploadFile):
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET'),
        secure=True
    )
    result = upload(image.file, folder="contacts")
    return result['secure_url']

    