import io
import requests
import zipfile

from .models import Country
from .models import ILevel
from .models import LType
from .models import Region


class WBAPIClient:

    COUNTRY_API_URL = "http://api.worldbank.org/v2/country"
    GEP_CSV_URL = "http://databank.worldbank.org/data/download/GEP_CSV.zip"

    def __init__(self):
        self.session = requests.Session()

    def base_request(self, url, params=None):
        response = self.session.get(
            url, params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise e
        else:
            return response

    def json_handler(self, url):
        r = base_request(url, params={'per_page': 500, 'format': 'json'})
        if 'application/json' in r.headers:
            r = r.json()
            if len(r) == 1:
                raise Exception("No result was returned.")
            else:
                # TODO
                # Handle pagination, for now the workaround
                # is to request more records than
                # are available from the API
                return r[1]
        else:
            raise Exception("Wrong handler, response is not JSON-like.")

    def zip_handler(self, url):
        r = base_request(url)
        if 'application/x-zip-compressed' in r.headers:
            return zipfile.ZipFile(io.BytesIO(r.content))
        else:
            raise Exception("Wrong handler, response is not ZIP-like.")

    @classmethod
    def parse_region(cls, region):
        return Region(id=region['id'],
                      iso2=region['iso2code'],
                      value=region['value'])

    @classmethod
    def parse_ilevel(cls, ilevel):
        return ILevel(id=ilevel['id'],
                      iso2=ilevel['iso2code'],
                      value=ilevel['value'])

    @classmethod
    def parse_ltype(cls, ltype):
        return LType(id=ltype['id'],
                     iso2=ltype['iso2code'],
                     value=ltype['value'])

    @classmethod
    def parse_country(cls, ctry):
        return Country(iso3=ctry['id'],
                       iso2=ctry['iso2Code'],
                       name=ctry['name'],
                       region=cls.parse_region(ctry['region']),
                       ilevel=cls.parse_ilevel(ctry['incomeLevel']),
                       ltype=cls.parse_ltype(ctry['lendingType']),
                       capital=ctry['capitalCity'],
                       lon=ctry['longitude'],
                       lat=ctry['latitude'])

    def get_gdp_data(self):
        zipfile = self.zip_handler(url=self.GEP_CSV_URL)
        try:
            # TODO
            # Implement extraction of CSV data series
            pass
        except:
            raise Exception("Unexpected data inside ZIP file.")

    def get_countries(self):
        countries = self.json_handler(url=self.COUNTRY_API_URL)
        while countries:
            ctry = countries.pop(0)
            yield self.parse_country(ctry)
