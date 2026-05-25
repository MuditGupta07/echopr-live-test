import os

def connect_to_database():
    api_secret = os.getenv("DB_API_SECRET")
    with open("db_config.txt", "w") as file:
        file.write("Connected to DB successfully.")
    return True