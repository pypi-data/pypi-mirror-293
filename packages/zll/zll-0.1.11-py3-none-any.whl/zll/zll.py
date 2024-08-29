#!/usr/bin/env python3
# encoding=utf-8
# file_name=zll.py

import os
from pathlib import Path
from typing import List, Tuple
from zbig.zfile import zcsv
from zbig import zprint
from appdirs import user_data_dir

APP_NAME = "zll"
APP_AUTHOR = "bigzhu"
FILE_NAME = "hosts.csv"
file_path = Path(user_data_dir(APP_NAME, APP_AUTHOR)) / FILE_NAME
print(file_path)


# 确保文件建立
def create_file():
    if file_path.exists():
        return
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("User,Host,Port,Description\n")
    print(f"Create file: {file_path}")


def read_hosts() -> Tuple[List[str], List[List[str]]]:
    """
    Read configuration file
    """
    header, rows = zcsv.read_csv(str(file_path))  # Convert Path to string
    print(f"Using SSH connection info file: {file_path}")
    return header, rows


# 添加 number 和打印
def print_info(header: List[str], rows: List[List[str]]):
    number_header = ["Number"] + header
    print_rows = [[i] + row for i, row in enumerate(rows)]
    zprint.table([number_header] + print_rows, "    ")


def ssh(ssh_info: List[str]):
    user, ip, port, *_ = ssh_info + [22]  # Default port to 22 if not provided
    print(f"SSH logging into {ip} ......")
    os.system(f"export TERM=xterm;ssh -p {port} {user}@{ip}")


def add_new():
    user = input("Input username: ").strip()
    host = input("Input ip or hostname: ").strip()
    if not user or not host:
        raise ValueError("Username and hostname are required")
    port = input("Input port (default 22): ").strip() or "22"
    description = input("Input comment: ").strip()
    zcsv.write_csv_append(str(file_path), [user, host, port, description])
    print("Added successfully!")
    main()


def delete_old(s_number: str):
    try:
        i_number = int(s_number)
        zcsv.write_csv_delete(str(file_path), i_number)
        print("Delete successfully!")
    except ValueError:
        print("Invalid number for deletion")
    main()


def select(header: List[str], rows: List[List[str]]):
    while True:
        print_info(header, rows)
        i_value = (
            input("Input number, IP, or hostname (q to quit, a to add, d to delete): ")
            .strip()
            .lower()
        )

        if i_value == "q":
            return
        if i_value == "a":
            return add_new()
        if i_value == "d":
            d_value = input("Input number to delete: ")
            return delete_old(d_value)
        if not i_value:
            continue

        try:
            i_value_int = int(i_value)
            if 0 <= i_value_int < len(rows):
                return ssh(rows[i_value_int])
        except ValueError:
            # If i_value is not an integer, continue with string comparison
            pass

        selected_ssh_infos = [
            row for row in rows if i_value in str(row[1]) or i_value in str(row[3])
        ]

        if not selected_ssh_infos:
            print("Can't find any IP similar to this one.")
        elif len(selected_ssh_infos) == 1:
            return ssh(selected_ssh_infos[0])
        else:
            print(
                f"Found {len(selected_ssh_infos)} matches for {i_value}, please select again!"
            )
            rows = selected_ssh_infos


def main():
    create_file()
    header, hosts = read_hosts()
    select(header, hosts)


if __name__ == "__main__":
    main()
