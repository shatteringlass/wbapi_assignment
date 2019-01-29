#! /usr/bin/env python3
import configparser
import glob
import os
import sys

from wbapi import db


def main():
    os.chdir(sys.path[0])
    c = configparser.ConfigParser()
    c.read('config.ini')
    # d = db.DatabaseManager(
    #    dbname=c['DATABASE']['dbname'], user=c['DATABASE']['user'], create_tbl=True)
    d = db.DatabaseManager(
        dbname=c['DATABASE']['dbname'], user=c['DATABASE']['user'])
    for fp in sorted(glob.glob('wbapi/sql/questions/*.sql')):
        # Load all available queries into the DB Manager object
        d.add_query(fp)
    for n, q in d.get_query().items():
        # Run all queries stored inside the DB Manager
        columns, records = d.run_query(n)
        print(columns)
        for r in records:
            print(r)


if __name__ == '__main__':
    main()
