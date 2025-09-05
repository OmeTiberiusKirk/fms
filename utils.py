import os
import argparse


def getEnv() -> dict[str:str]:
    sv = os.getenv("DB_SERVER")
    db = os.getenv("DB_NAME")
    u = os.getenv("DB_USER")
    pw = os.getenv("DB_PASS")

    if sv is None:
        raise ValueError("You need to specify a server name.")
    if db is None:
        raise ValueError("You need to specify a datbase name.")
    if u is None:
        raise ValueError("You need to specify a username.")
    if pw is None:
        raise ValueError("You need to specify a password.")

    print("-------- env variables ----------")
    print(f"Server: {sv}")
    print(f"Database: {db}")
    print(f"Username: {u}")
    print(f"Password: {pw}")

    return {"sv": sv, "db": db, "u": u, "pw": pw}


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--table", type=str, help="ระบุชื่อตาราง")
    parser.add_argument("-o", "--order_by", type=str, help="ตัวเลือกสำหรับจัดระเบียบ")
    parser.add_argument(
        "-s",
        "--sort",
        type=str,
        help="ตัวเลือกสำหรับเรียง (ค่าเริ่มต้น asc)",
        default="asc",
    )
    parser.add_argument("-n", "--number", type=str, help="ตัวเลือกสำหรับระบุจำนวนแถว")
    args = parser.parse_args()

    if args.table is None:
        raise ValueError("You need to specify a table.")

    print("-------- args ----------")
    print(args.__dict__)

    return args.__dict__
