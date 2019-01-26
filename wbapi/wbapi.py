import io
import csv

import requests
import zipfile

from .models import Country
from .models import ILevel
from .models import LType
from .models import Region
from .models import GDPDatapoint


class WBAPIClient:

    COUNTRY_API_URL = "http://api.worldbank.org/v2/country"
    GDP_CSV_URL = "http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv"
    GDP_CSV_FILENAME = "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_10363296.csv"

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
        r = self.base_request(url, params={'per_page': 500, 'format': 'json'})
        if 'application/json' in r.headers['Content-Type']:
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
        mime_zip = ['application/zip',
                    'application/x-zip',
                    'application/x-zip-compressed',
                    'application/octet-stream',
                    'application/x-compress',
                    'application/x-compressed',
                    'multipart/x-zip']
        r = self.base_request(url)
        if r.headers['Content-Type'] in mime_zip:
            zf = zipfile.ZipFile(io.BytesIO(r.content))
            return zf
        else:
            raise Exception("Wrong handler, response is not ZIP-like.")

    @classmethod
    def parse_region(cls, region):
        return Region(_id=region['id'],
                      iso2=region['iso2code'],
                      value=region['value'])

    @classmethod
    def parse_ilevel(cls, ilevel):
        return ILevel(_id=ilevel['id'],
                      iso2=ilevel['iso2code'],
                      value=ilevel['value'])

    @classmethod
    def parse_ltype(cls, ltype):
        return LType(_id=ltype['id'],
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

    @classmethod
    def parse_gdp_data(cls, row, start_year=1960, end_year=2019):
        ctry_name = row["Country Name"]
        ctry_code = row["Country Code"]
        years = range(start_year, end_year)
        return [GDPDatapoint(ctry_name=ctry_name,
                             ctry_code=ctry_code,
                             year=y,
                             value=row[str(y)]) for y in years]

    def get_gdp_data(self):
        try:
            csvfile = self.zip_handler(url=self.GDP_CSV_URL)  \
                          .open(self.GDP_CSV_FILENAME)  \
                          .read()  \
                          .decode('utf-8-sig')  \
                          .splitlines()[4:]
            rows = csv.DictReader(csvfile, delimiter=",", quotechar="\"")
            result = list()
            for dct in rows:
                result.extend(self.parse_gdp_data(dct))
            return result
        except:
            raise Exception("Unexpected data inside ZIP file.")

    def get_countries(self):
        countries = self.json_handler(url=self.COUNTRY_API_URL)
        while countries:
            ctry = countries.pop(0)
            yield self.parse_country(ctry)
