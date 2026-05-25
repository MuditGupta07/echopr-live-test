import os
import sqlite3

# DIRTY CODE: This will trigger multiple EchoPR rules
def get_user_data(user_id):
    # DANGEROUS: SQL Injection risk
    query = "SELECT * FROM users WHERE id = " + user_id
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchone()
    # DANGEROUS: Not closing the connection
    return data

def connect_to_api():
    # CRITICAL: Hardcoded Secret
    api_key = "sk-live-51Mz2w4L9p0qR8sT7uV6wX5yZ4"
    url = "https://api.payments.com/process"
    
    # INSECURE: SSL verification disabled
    response = requests.post(url, json={"key": api_key}, verify=False)
    return response.json()

def process_logs(log_file):
    # INEFFICIENT: Reading entire file into memory
    with open(log_file, 'r') as f:
        logs = f.readlines()
        
    for log in logs:
        # CODE SMELL: Generic print statements instead of logging
        print("Processing: " + log)
        if "error" in log:
            # BAD PRACTICE: Catching bare Exception
            try:
                raise Exception("Fatal error")
            except:
                pass

# UNUSED CODE: Leftover dead code
def old_function_not_used():
    x = 1
    y = 2
    return x + y

data = get_user_data("123")
