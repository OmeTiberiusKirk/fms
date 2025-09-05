# import argparse
import pyodbc
import pandas as pd
import utils
import math


if __name__ == "__main__":
    try:
        env = utils.getEnv()
        args = utils.getArgs()
        size = 5000

        cnxn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={env['sv']};DATABASE={env["db"]};UID={env["u"]};PWD={env["pw"]}"
        cnxn = pyodbc.connect(cnxn_str)
        cursor = cnxn.cursor()

        print("-------- Database connected. ---------")

        query = f"SELECT COUNT(*) FROM {args['table']}"
        cursor.execute(query)
        totalRows = cursor.fetchval()
        n: int = math.ceil(totalRows / size)

        for i in range(n):
            output_csv_file = f"{args['table']}{"" if i == 0 else "_" + str(i)}.csv"

            # Fetch data from the specified table
            query = f"""
                SELECT * FROM {args['table']} 
                ORDER BY HS_NO 
                OFFSET {i * size} ROWS
                FETCH NEXT {size} ROWS ONLY
            """
            cursor.execute(query)
            # Fetch all rows
            rows = cursor.fetchall()

            # Get column names for the DataFrame
            columns = [column[0] for column in cursor.description]
            # Create a Pandas DataFrame
            df = pd.DataFrame.from_records(rows, columns=columns)

            # Export DataFrame to CSV
            df.to_csv(output_csv_file, index=False, encoding="utf-8", sep="|")

        # query = f"SELECT * FROM {args['table']}"
        # if args['order_by']:
        #     query = query + f" ORDER BY {args['order_by']}"
        # cursor.execute(query)
    except pyodbc.Error as ex:
        print(ex)
    except Exception as e:
        print(e)
    finally:
        if "cnxn" in locals() and cnxn:
            cnxn.close()
