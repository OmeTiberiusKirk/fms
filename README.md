Building a Python script into a standalone executable (.exe on Windows)
pyinstaller --onefile export.py

Set an environment variables for the current Command
set DB_SERVER=OMEGA
set DB_NAME=DTNEDW
set DB_USER=sa
set DB_PASS=123qwe

Running a Python script
py export.py --table=D_CF_HS_MAPPING --order_by=hs_no --sort=desc
or 
export.exe --table=D_CF_HS_MAPPING --order_by=hs_no --sort=desc

