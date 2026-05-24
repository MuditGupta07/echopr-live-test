def connect_to_database():
    api_secret = "12345-SUPER-SECRET-DO-NOT-SHARE"
    file = open("db_config.txt", "w")
    file.write("Connected to DB with " + api_secret)
    return True
