import psycopg2

from wbapi import WBAPIClient

dbname = "wbdb"
uid = "wbdb_user"

pfields = {'Country': ['iso3', 'iso2', 'name', 'reg_id', 'ilevel_id', 'ltype_id', 'capital', 'lon', 'lat'],
           'Region': ['id', 'iso2', 'value'],
           'ILevel': ['id', 'iso2', 'value'],
           'LType': ['id', 'iso2', 'value']
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
    def insert_statement(self):
        sql = f"INSERT INTO {self.table_name} ({', '.join(self.fields)}) VALUES ({self.mapped_values});"
        return sql, self.state


def populate_db():
    conn = psycopg2.connect(f"dbname={dbname} user={uid}")
    cur = conn.cursor()
    with WBAPIClient() as c:
        for country in c.get_countries():
            cur.execute(ObjectMapper(country).insert_statement)
            cur.execute(ObjectMapper(country.region).insert_statement)
            cur.execute(ObjectMapper(country.ltype).insert_statement)
            cur.execute(ObjectMapper(country.ilevel).insert_statement)
            conn.commit()
    cur.close()
    conn.close()
