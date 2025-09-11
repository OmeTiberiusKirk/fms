import os
import csv
from utils import connectDB
import pyodbc
import logging

if __name__ == "__main__":
    # Configure basic logging to a file
    logging.basicConfig(
        filename="app.log",  # Name of the log file
        level=logging.INFO,  # Minimum logging level to capture (e.g., INFO, DEBUG, WARNING, ERROR, CRITICAL)
        filemode="w",  # 'a' for append (default), 'w' for overwrite
        format="%(asctime)s - %(levelname)s - %(message)s",  # Format of log messages
    )

    directory_path = "csv"  # Replace with your directory

    try:

        cnxn, cursor = connectDB()

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path):  # Check if it's a file, not a subdirectory
                table_name = filename.split("-")[0]
                with open(file_path, "r", encoding="utf-8") as f:  # 'r' for read mode
                    reader = csv.reader(f, delimiter="¦")
                    header = next(reader)
                    for row in reader:
                        try:
                            insert_query = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                            cursor.execute(insert_query, *row)
                            print(f"inserted in to {table_name}")
                            print(f"row = {row}")
                        except pyodbc.Error as e:
                            print(e.args[1])
                            logging.error(e.args[1])
        cnxn.commit()
        cursor.close()
    except pyodbc.Error as e:
        print(e)
        logging.error(e.args[1])
    except Exception as e:
        print(e)
    finally:
        if "cnxn" in locals() and cnxn:
            cnxn.close()
            print("Database disconnected.")
