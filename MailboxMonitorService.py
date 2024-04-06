from flask import Flask, request
import threading
from exchangelib import Credentials, Account, DELEGATE

app = Flask(__name__)

# Dummy credentials (replace with actual credentials)
USERNAME = "dummy_user"
PASSWORD = "dummy_password"

# Dictionary to store monitored mailboxes and their status
monitored_mailboxes = {}
# Initialize Redis client for centralized state management
redis_client = Redis(host='redis', port=6379, db=0)  # Use Redis running on a separate server or container

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
     # Register the event handler function
    listener = Listener(account)
    listener.streaming_event_received += handle_new_email

    # Start listening for new email events
    listener.listen()

    # Store the subscription in the monitored_mailboxes dictionary
   
    monitored_mailboxes[mailbox] = {'mailboax': mailbox, 'last_event_time': None}
    # Store the subscription ID in the centralized state management (Redis)
    redis_client.set(mailbox, listener.subscription_id)

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
    #this is for loadbalancing server logic
    if not redis_client.exists(mailbox):
            # Start monitoring the mailbox
            monitor_mailbox(mailbox)
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
    #This is for central managed state management
    if redis_client.exists(mailbox):
            # Stop monitoring the mailbox (unsubscribe from events)
            subscription_id = redis_client.get(mailbox)
            # Code to unsubscribe from events goes here (not shown in this example)
            # Remove the mailbox from centralized state management
            redis_client.delete(mailbox)
            return f"Monitoring stopped for {mailbox}", 200
        else:
            return f"{mailbox} is not being monitored", 400
@app.route("/status/timeframe", methods=["GET"])
def status_timeframe():
    # Dummy authentication (replace with actual authentication mechanism)
    username = request.headers.get("Username")
    password = request.headers.get("Password")
    if username != USERNAME or password != PASSWORD:
        return "Unauthorized", 401

    mailbox = request.args.get("mailbox")
    if mailbox in monitored_mailboxes:
        last_event_time = monitored_mailboxes[mailbox]['last_event_time']
        if last_event_time is not None:
            current_time = datetime.now()
            # Adjust this threshold as needed based on your application requirements
            if (current_time - last_event_time).total_seconds() <= 60:  # Check if mailbox was active in the last 60 seconds
                return f"{mailbox} is actively being monitored", 200
            else:
                return f"{mailbox} is not actively being monitored", 404
        else:
            return f"{mailbox} is not actively being monitored", 404
    else:
        return f"{mailbox} is not being monitored", 400

@app.route("/status/mailarrival", methods=["GET"])
def status_mailarrival():
    # Dummy authentication (replace with actual authentication mechanism)
    username = request.headers.get("Username")
    password = request.headers.get("Password")
    if username != USERNAME or password != PASSWORD:
        return "Unauthorized", 401

    mailbox = request.args.get("mailbox")
    if mailbox in monitored_mailboxes:
        last_event_time = monitored_mailboxes[mailbox]['last_event_time']
        account = monitored_mailboxes[mailbox]['listener']._account
        if last_event_time is not None:
            # Fetch the latest mail arrival time in the mailbox
            latest_mail_arrival_time = account.inbox.filter(datetime_received__gt=last_event_time).order_by('-datetime_received').first().datetime_received
            current_time = datetime.now()
            if latest_mail_arrival_time is not None and (current_time - latest_mail_arrival_time).total_seconds() <= 60:
                return f"{mailbox} is actively being monitored", 200
            else:
                return f"{mailbox} is not actively being monitored", 404
        else:
            return f"{mailbox} is not actively being monitored", 404
    else:
        return f"{mailbox} is not being monitored", 400

if __name__ == "__main__":
    app.run(debug=True)
