import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SERVER = os.getenv("EMAIL_SERVER")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
NOTIF_ENDPOINT = os.getenv("NOTIF_ENDPOINT", "http://localhost:8000/notify")
