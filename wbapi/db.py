import psycopg2
from .wbapi import WBAPIClient
import pprint

persistent_fields = {'Country': [],
                     }


class ObjectMapper:
    def __init__(self, orig):
        self.orig = orig
        self.tmp = {}
        self.items, self.fields = self._gatherState()

    def _gatherState(self):
        adaptee_name = self.orig.__class__.__name__
        fields = sorted([(field, getattr(self.orig, field))
                         for field in persistent_fields[adaptee_name]])
        items = []
        for item, value in fields:
            items.append(item)
        return items, fields

    def getTableName(self):
        return self.orig.__class__.__name__

    def getMappedValues(self):
        tmp = []
        for i in self.items:
            tmp.append("%%(%s)s" % i)
        return ", ".join(tmp)

    def getValuesDict(self):
        return dict(self.fields)

    def getFields(self):
        return self.items

    def generateInsert(self):
        qry = "INSERT INTO"
        qry += " " + self.getTableName() + " ("
        qry += ", ".join(self.getFields()) + ") VALUES ("
        qry += self.getMappedValues() + ")"
        return qry, self.getValuesDict()


c = WBAPIClient()
pprint.pprint(list(c.get_countries()), indent=4)
