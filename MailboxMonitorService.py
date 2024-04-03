from flask import Flask, request
import threading
from exchangelib import Credentials, Account, DELEGATE

app = Flask(__name__)

# Dummy credentials (replace with actual credentials)
USERNAME = "dummy_user"
PASSWORD = "dummy_password"

# Dictionary to store monitored mailboxes and their status
monitored_mailboxes = {}

# Function to monitor a mailbox
def monitor_mailbox(mailbox):
    # Set up Exchange Web Services credentials
    credentials = Credentials(username=USERNAME, password=PASSWORD)

    # Connect to the Exchange server
    account = Account(primary_smtp_address=mailbox, credentials=credentials, autodiscover=True, access_type=DELEGATE)

    # Define a callback function to handle new email notifications
    def handle_new_email(notification):
        # Process the notification (e.g., print the subject of the new email)
        print("New email received in", mailbox, ":", notification.item.subject)

    # Subscribe to receive notifications for new emails in the inbox folder
    subscription = account.inbox.subscribe(callback=handle_new_email)

    # Store the subscription in the monitored_mailboxes dictionary
    monitored_mailboxes[mailbox] = subscription

# API endpoint to start monitoring a mailbox
@app.route("/start_monitoring", methods=["POST"])
def start_monitoring():
    # Dummy authentication (replace with actual authentication mechanism)
    username = request.headers.get("Username")
    password = request.headers.get("Password")
    if username != USERNAME or password != PASSWORD:
        return "Unauthorized", 401

    mailbox = request.json.get("mailbox")
    if mailbox not in monitored_mailboxes:
        # Start a new thread to monitor the mailbox
        thread = threading.Thread(target=monitor_mailbox, args=(mailbox,))
        monitored_mailboxes[mailbox] = thread
        thread.start()
        return f"Monitoring started for {mailbox}", 200
    else:
        return f"{mailbox} is already being monitored", 400

# API endpoint to stop monitoring a mailbox
@app.route("/stop_monitoring", methods=["POST"])
def stop_monitoring():
    # Dummy authentication (replace with actual authentication mechanism)
    username = request.headers.get("Username")
    password = request.headers.get("Password")
    if username != USERNAME or password != PASSWORD:
        return "Unauthorized", 401

    mailbox = request.json.get("mailbox")
    if mailbox in monitored_mailboxes:
        # Stop the thread monitoring the mailbox
        monitored_mailboxes[mailbox].join()
        del monitored_mailboxes[mailbox]
        return f"Monitoring stopped for {mailbox}", 200
    else:
        return f"{mailbox} is not being monitored", 400

if __name__ == "__main__":
    app.run(debug=True)
