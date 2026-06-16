import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
NYC_OPEN_DATA_APP_TOKEN = os.getenv("NYC_OPEN_DATA_APP_TOKEN", "")
