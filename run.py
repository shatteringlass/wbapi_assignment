from wbapi import db
import glob


def main():
    # d = db.DatabaseManager(create_tbl=True)
    d = db.DatabaseManager()
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
