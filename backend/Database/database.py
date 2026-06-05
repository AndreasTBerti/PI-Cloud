from dotenv import load_dotenv
import os
from supabase import create_client

#from backend.Models.model import ClimateData

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
print(url)
print(key[:20])

supabase = create_client(
        url, key
    )


def save_data(data):

    insert = supabase.table(
        "Sensor"
    ).insert({
        "sensor_id": data.sensor_id,
        "temperature": data.temperatura,
        "humidity": data.umidade
    }).execute()


if __name__ == "__main__":
    pass