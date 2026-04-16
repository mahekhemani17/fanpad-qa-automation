import os
from dotenv import load_dotenv

load_dotenv()

ARTIST = {
    "email": os.getenv("ARTIST_EMAIL"),
    "password": os.getenv("ARTIST_PASSWORD"),
    "base_url": os.getenv("ARTIST_BASE_URL"),
}