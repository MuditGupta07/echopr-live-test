def connect_to_database():
    # Hardcoded dummy API key for testing
    api_secret = "12345-SUPER-SECRET-DO-NOT-SHARE"

    file = open("db_config.txt", "w")
    file.write("Connected to DB with " + api_secret)

    # Intentionally forgot to close the file to trigger a warning
    return True
