__title__ = "wbapi-py"
__version__ = "0.1"
__author__ = "shatteringlass"
__license__ = "MIT"

from .wbapi import WBAPIClient

c = WBAPIClient()
c.get_country('it')
