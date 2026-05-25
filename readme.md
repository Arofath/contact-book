# Introduction

To run this application, type following commands:

```bash
# for development
uvicorn main:app --reload --port=8000

# for production
uvicorn main:app --port=8000 --workers=4# contact-book
