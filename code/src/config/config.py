import os
from dotenv import load_dotenv

load_dotenv()

NOTIF_ENDPOINT = os.getenv("NOTIF_ENDPOINT", "http://localhost:8000/notify")
