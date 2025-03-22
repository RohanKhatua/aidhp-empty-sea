import requests
from models import NotificationRequest
from config.config import NOTIF_ENDPOINT

def send_notification(notification: NotificationRequest):
    """Sends a notification when processing is complete."""
    response = requests.post(NOTIF_ENDPOINT, json=notification.dict())
    return response.json()

if __name__ == "__main__":
    print(send_notification(NotificationRequest(email_id="123", status="Processed", request_types=[{"type":"A", "subType":"B"}],teams_to_notify=["Payments"])).model_dump_json())  # For testing
