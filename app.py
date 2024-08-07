from flask import Flask, request, redirect, url_for
from email_service import send_email, retrieve_emails, init_db
import schedule
import time
import threading

app = Flask(__name__)

db = init_db()

@app.route('/')
def home():
    return "Microsoft Graph Email API Integration"

@app.route('/send-email', methods=['POST'])
def send_email_route():
    data = request.json
    recipient = data['recipient']
    subject = data['subject']
    body = data['body']
    send_email(recipient, subject, body)
    return "Email sent successfully!"

def schedule_retrieve_emails():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().hour.do(retrieve_emails, db)

if __name__ == '__main__':
    threading.Thread(target=schedule_retrieve_emails).start()
    app.run(debug=True)