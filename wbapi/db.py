import psycopg2

from .models import adapters
from .wbapi import WBAPIClient

pfields = {'Country': [],
           'Region': [],
           'ILevel': [],
           'LType': []
           }


class ObjectMapper:
    def __init__(self, obj):
        self._obj = obj
        self._name = self.orig.__class__.__name__
        self._pfields = pfields[self._name]
        self._state = {field: getattr(self.orig, field)
                       for field in self.pfields}

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
        qry = f"INSERT INTO {self.table_name} ({', '.join(self.fields)}) VALUES ({self.mapped_values});"
        return qry, self.state


psycopg2.extensions.adapters.update(adapters)

c = WBAPIClient()
for country in c.get_countries():
    print(psycopg2.extensions.adapt(country).insert_statement)
