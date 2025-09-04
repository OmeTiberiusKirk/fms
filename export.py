import argparse
import pyodbc
import pandas as pd

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--server", type=str, help="Your server")
        parser.add_argument("--database", type=str, help="Your database")
        parser.add_argument("--table", type=str, help="Your table")
        parser.add_argument("--username", type=str, help="Your username")
        parser.add_argument("--password", type=str, help="Your password")
        args = parser.parse_args()

        print(f"Server: {args.server}")
        print(f"Database: {args.database}")
        print(f"Table: {args.database}")
        print(f"Username: {args.username}")
        print(f"Password: {args.password}")
        output_csv_file = 'output_data.csv'

        if (
            args.server
            and args.database
            and args.table
            and args.username
            and args.password
        ):
            cnxn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={args.server};DATABASE={args.database};UID={args.username};PWD={args.password}"
            cnxn = pyodbc.connect(cnxn_str)
            cursor = cnxn.cursor()

            print("-------- Database connected. ---------")

            # Fetch data from the specified table
            query = f"SELECT * FROM {args.table}"
            cursor.execute(query)

            # Get column names for the DataFrame
            columns = [column[0] for column in cursor.description]
            print(columns)

            # Fetch all rows
            rows = cursor.fetchall()

            # Create a Pandas DataFrame
            df = pd.DataFrame.from_records(rows, columns=columns)

            # Export DataFrame to CSV
            df.to_csv(output_csv_file, index=False, encoding='utf-8')
    except pyodbc.Error as ex:
        print(ex.args[1])
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if "cnxn" in locals() and cnxn:
            cnxn.close()
