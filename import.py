import os
import csv
from utils import connectDB
import pyodbc

if __name__ == "__main__":
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
                        insert_query = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                        cursor.execute(insert_query, *row)

        cnxn.commit()
        cursor.close()
    except Exception as e:
        print(e)
    except pyodbc.Error as e:
        print(e)   
    finally:
        if "cnxn" in locals() and cnxn:
            cnxn.close()
            print("Database disconnected.")
