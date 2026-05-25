import os
import sqlite3
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# DIRTY CODE: This will trigger multiple EchoPR rules
def get_user_data(user_id):
    try:
        # Use a 'with' statement for the connection to ensure it's closed
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            # Use a parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
            data = cursor.fetchone()
            return data
    except sqlite3.Error as e:
        logging.error(f"Database error while fetching user data for ID {user_id}: {e}")
        return None

def connect_to_api():
    # Load API key from environment variables for security
    api_key = os.getenv("PAYMENTS_API_KEY")
    if not api_key:
        logging.critical("PAYMENTS_API_KEY environment variable not set. Cannot connect to API securely.")
        raise ValueError("API Key is not configured.")

    url = "https://api.payments.com/process"
    
    try:
        # Ensure SSL verification is enabled for secure communication
        response = requests.post(url, json={"key": api_key}) # Removed verify=False
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None
    except ValueError as e:
        logging.error(f"Failed to decode API response JSON: {e}")
        return None

def process_logs(log_file):
    try:
        # Process large log files line by line to prevent OutOfMemory errors
        with open(log_file, 'r') as f:
            for line_num, log_line in enumerate(f, 1): # Start line numbers from 1
                # Use a proper logging framework instead of print statements
                logging.info(f"Processing line {line_num}: {log_line.strip()}")
                if "error" in log_line.lower():
                    # Catch specific exception types for better error handling and debugging
                    try:
                        raise ValueError(f"Error keyword detected in log line {line_num}")
                    except ValueError as e:
                        logging.error(f"Application specific error during log processing: {e} - Content: '{log_line.strip()}'")
                    except Exception as e:
                        logging.exception(f"An unexpected error occurred while processing log line {line_num}: '{log_line.strip()}'")
    except FileNotFoundError:
        logging.error(f"Log file not found: {log_file}")
    except IOError as e:
        logging.error(f"Error reading log file {log_file}: {e}")
    except Exception as e:
        logging.exception(f"An unexpected error occurred while processing log file: {log_file}")

# Removed 'old_function_not_used' as it was dead code.

if __name__ == "__main__":
    # Example usage of the refactored functions
    user_data = get_user_data("123")
    if user_data:
        logging.info(f"Retrieved user data: {user_data}")
    else:
        logging.warning("Failed to retrieve user data or user not found.")

    try:
        api_response = connect_to_api()
        if api_response:
            logging.info(f"Successfully connected to API. Response: {api_response}")
        else:
            logging.warning("API connection failed or returned no data.")
    except ValueError as e:
        logging.critical(f"API configuration error: {e}")

    # Create a dummy log file for testing if it doesn't exist
    if not os.path.exists("application.log"):
        with open("application.log", "w") as f:
            f.write("INFO: Application started\n")
            f.write("DEBUG: Some debug info\n")
            f.write("WARNING: A potential issue detected\n")
            f.write("ERROR: Failed to process request 123\n")
            f.write("INFO: Application finished\n")

    process_logs("application.log")