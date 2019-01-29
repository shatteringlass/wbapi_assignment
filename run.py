#! /usr/bin/env python3
import os
import glob
import configparser

from wbapi import db


def main():
    c = configparser.ConfigParser()
    c.read('config.ini')
    # d = db.DatabaseManager(
    #    dbname=c['DATABASE']['dbname'], user=c['DATABASE']['user'], create_tbl=True)
    d = db.DatabaseManager(
        dbname=c['DATABASE']['database_name'], uid=c['DATABASE']['username'])
    for fp in sorted(glob.glob('wbapi/sql/questions/*.sql')):
        d.add_query(fp)
    for n, q in d.get_query().items():
        print(f"\n\nResults:")
        try:
            for record in d.run_query(n):
                print(record)
        except:
            print("None")
            continue


if __name__ == '__main__':
    main()
