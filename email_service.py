import requests
import pymongo
from datetime import datetime, timedelta

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
TENANT_ID = 'your-tenant-id'
REDIRECT_URI = 'http://localhost:8000/callback'
AUTH_URL = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
SCOPES = ['https://graph.microsoft.com/.default']

MONGO_URI = 'your-mongodb-uri'
DATABASE_NAME = 'email_db'
COLLECTION_NAME = 'emails'

def init_db():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db

def get_access_token():
    response = requests.post(AUTH_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': ' '.join(SCOPES),
    })
    response.raise_for_status()
    return response.json()['access_token']

def send_email(recipient, subject, body):
    token = get_access_token()
    url = 'https://graph.microsoft.com/v1.0/me/sendMail'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }
    response = requests.post(url, headers=headers, json=email_data)
    response.raise_for_status()

def retrieve_emails(db):
    token = get_access_token()
    url = 'https://graph.microsoft.com/v1.0/me/messages'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    yesterday = datetime.utcnow() - timedelta(days=1)
    params = {
        '$filter': f'receivedDateTime ge {yesterday.isoformat()}Z'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    emails = response.json().get('value', [])
    for email in emails:
        db[COLLECTION_NAME].insert_one(email)
