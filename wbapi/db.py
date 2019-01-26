import psycopg2

from .wbapi import WBAPIClient

dbname = "wbapi"
uid = "federico"

pfields = {'Country': ['iso3', 'iso2', 'name', 'reg_id', 'ilevel_id', 'ltype_id', 'capital', 'lon', 'lat'],
           'Region': ['id', 'iso2', 'value'],
           'ILevel': ['id', 'iso2', 'value'],
           'LType': ['id', 'iso2', 'value'],
           'GDPDatapoint': ['ctry_name', 'ctry_code', 'year', 'value']
           }


class ObjectMapper:
    def __init__(self, obj):
        self._obj = obj
        self._name = self._obj.__class__.__name__
        self._pfields = pfields[self._name]
        self._state = {field: getattr(self._obj, field)
                       for field in self._pfields}

    @property
    def table_name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def fields(self):
        return list(self.state.keys())

    @property
    def mapped_values(self):
        return ", ".join([f"%({i})s" for i in self.fields])

    @property
    def create_statement(self):
        sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({' varchar, '.join(self.fields)} varchar);"
        return sql

    @property
    def insert_statement(self):
        sql = f"INSERT INTO {self.table_name} ({', '.join(self.fields)}) VALUES ({self.mapped_values}) ON CONFLICT DO NOTHING;"
        return sql, self.state


def export_dml(dml, file=None):
    if not(file):
        print(dml)
    else:
        # TODO: implement export to file
        # to allow manual editing
        pass


class DatabaseManager:

    def __init__(self, dbname=dbname, user=uid, create_tbl=False):
        self.conn = psycopg2.connect(f"dbname={dbname} user={uid}")
        if create_tbl:
            self.populate_db()
        self.queries = dict()

    def __del__(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def add_query(self, sql_file):
        n = len(self.queries)
        with open(sql_file, 'r') as f:
            self.queries[n+1] = f.read()

    def get_query(self, number=None):
        if number:
            return self.queries.get(number)
        else:
            return self.queries

    def run_query(self, number):
        sql = self.get_query(number)
        cur = self.conn.cursor()
        print(f"\n\nNow running query #{number} with statement:\n\n{sql}\n\n")
        cur.execute(sql)
        return cur if cur.rowcount > 0 else []

    def populate_db(self):
        cur = self.conn.cursor()
        c = WBAPIClient()
        for i, country in enumerate(c.get_countries()):
            if i == 0:
                export_dml(ObjectMapper(country).create_statement)
                export_dml(ObjectMapper(country.region).create_statement)
                export_dml(ObjectMapper(country.ltype).create_statement)
                export_dml(ObjectMapper(country.ilevel).create_statement)
                input(
                    "Execute the DML code to create the tables, then press Enter to continue.")
            cur.execute(*ObjectMapper(country).insert_statement)
            cur.execute(*ObjectMapper(country.region).insert_statement)
            cur.execute(*ObjectMapper(country.ltype).insert_statement)
            cur.execute(*ObjectMapper(country.ilevel).insert_statement)
        for i, dp in enumerate(c.get_gdp_data()):
            if i == 0:
                export_dml(ObjectMapper(dp).create_statement)
                input(
                    "Execute the DML code to create the tables, then press Enter to continue.")
            cur.execute(*ObjectMapper(dp).insert_statement)
        self.conn.commit()
        cur.close()
        self.conn.close()
