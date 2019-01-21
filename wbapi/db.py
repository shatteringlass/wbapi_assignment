import psycopg2
from .wbapi import WBAPIClient
import pprint

c = WBAPIClient()
pprint.pprint(list(c.get_countries()),indent=4)
