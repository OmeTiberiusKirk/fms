from typing import TypedDict, List
import os
import shutil
import pyodbc
import argparse
from pyodbc import Row


class Env(TypedDict):
    sv: str
    db: str
    u: str
    pw: str


class Args(TypedDict):
    table: str
    order_by: str
    sort: str
    number: int
    sep: str
    size: int
    offset: int


def getEnv() -> Env:
    sv = os.getenv("DB_SERVER")
    db = os.getenv("DB_NAME")
    u = os.getenv("DB_USER")
    pw = os.getenv("DB_PASS")

    return {"sv": sv, "db": db, "u": u, "pw": pw}


def getArgs() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", type=str, help="table name")
    parser.add_argument("--order_by", type=str, help="ตัวเลือกสำหรับจัดระเบียบ")
    parser.add_argument(
        "--sort",
        type=str,
        help="ตัวเลือกสำหรับเรียง (ค่าเริ่มต้น asc)",
        default="asc",
    )
    parser.add_argument(
        "--offset",
        type=int,
        help="specifies the number of rows to skip before starting.",
        default=0,
    )
    parser.add_argument(
        "--number",
        type=int,
        default=10000,
        help="ตัวเลือกสำหรับระบุจำนวนแถวทั้งหมดที่ต้องการ",
    )
    parser.add_argument("--sep", type=str, default="¦", help="ตัวเลือกสำหรับตัวแบ่งแถว")
    parser.add_argument(
        "--size", type=int, default=1000, help="ตัวเลือกสำหรับจำนวนแถวต่อหน้า"
    )

    args = parser.parse_args()

    return args.__dict__


def connectDB():
    env = getEnv()
    cnxn_str = f"""
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={env['sv']};
        DATABASE={env["db"]};
        UID={env["u"]};
        PWD={env["pw"]};
    """
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()
    print("Database connected.")
    return cnxn, cursor


def createCSVDir():
    dir = "csv"
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    return dir
