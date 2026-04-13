from supabase import create_client
from dotenv import load_dotenv
from os import getenv

load_dotenv()

url: str = ""
key: str = getenv("DATABASE_API_KEY")

supabase = create_client(url, key)


def save_data(data):
    pass

if __name__ == "__main__":
    pass