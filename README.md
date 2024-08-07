# Microsoft Graph API Email Integration

This project demonstrates how to send and retrieve emails using the Microsoft Graph API. The retrieved emails are stored in MongoDB.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Naveenkumar1405/Kavida.ai.git
   cd kavida.ai

2.
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3.  pip install -r requirements.txt

4. python app.py

5. test with: 

    POST /send-email
{
    "recipient": "recipient@example.com",
    "subject": "Test Subject",
    "body": "Test Body"
}
