import psycopg2

from wbapi import WBAPIClient

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
        sql = f"INSERT INTO {self.table_name} ({', '.join(self.fields)}) VALUES ({self.mapped_values});"
        return sql, self.state


def populate_db():
    conn = psycopg2.connect(f"dbname={dbname} user={uid}")
    cur = conn.cursor()
    c = WBAPIClient()
    for i, country in enumerate(c.get_countries()):
        if i == 0:
            cur.execute(ObjectMapper(country).create_statement)
            cur.execute(ObjectMapper(country.region).create_statement)
            cur.execute(ObjectMapper(country.ltype).create_statement)
            cur.execute(ObjectMapper(country.ilevel).create_statement)
            conn.commit()
        cur.execute(*ObjectMapper(country).insert_statement)
        cur.execute(*ObjectMapper(country.region).insert_statement)
        cur.execute(*ObjectMapper(country.ltype).insert_statement)
        cur.execute(*ObjectMapper(country.ilevel).insert_statement)
    for i, dp in enumerate(c.get_gdp_data()):
        if i == 0:
            cur.execute(ObjectMapper(dp).create_statement)
            conn.commit()
        cur.execute(*ObjectMapper(dp).insert_statement)
    conn.commit()
    cur.close()
    conn.close()


populate_db()
