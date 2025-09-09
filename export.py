import pyodbc
import pandas as pd
import utils

if __name__ == "__main__":
    try:
        env = utils.getEnv()
        args = utils.getArgs()
        dir = utils.createCSVDir()

        cnxn, cursor = utils.connectDB()

        query = f"SELECT COUNT(*) FROM {args['table']}"
        cursor.execute(query)
        totalRows = cursor.fetchval()
        totalRows = totalRows if totalRows <= args["number"] else args["number"]

        i = 0
        while totalRows > 0:
            output_csv_file = f"{args['table']}-{i+1}.csv"
            # Fetch data from the specified table
            query = f"""
              SELECT * FROM {args['table']} 
              ORDER BY {args['order_by']} {args['sort']}
              OFFSET {i * args['size']} ROWS
              FETCH NEXT {args['size'] if args['size'] < totalRows else totalRows} ROWS ONLY
          	"""
            cursor.execute(query)

            rows = []
            for row in cursor:
                # Clean newline characters in Python
                cleaned_row = [
                    (
                        str(item).replace("\n", "").replace("\r", "")
                        if isinstance(item, str)
                        else item
                    )
                    for item in row
                ]
                rows.append(cleaned_row)

            # Get column names for the DataFrame
            columns = [column[0] for column in cursor.description]
            # Create a Pandas DataFrame
            df = pd.DataFrame.from_records(rows, columns=columns)
            # Export DataFrame to CSV
            df.to_csv(f"{dir}/{output_csv_file}", index=False, sep=args["sep"])
            print("--------- csv created successfully ---------")

            totalRows = totalRows - args["size"]
            i += 1
    except pyodbc.Error as ex:
        print(ex)
    except Exception as e:
        print(e)
    finally:
        if "cnxn" in locals() and cnxn:
            cnxn.close()
            print("Database disconnected.")
