from Database.database import save_data
from Processing.transform import transform_data


def run_pipeline(data: dict):
    processed_data: dict = transform_data(data)
    save_data(processed_data)

if __name__ == "__main__":
    pass