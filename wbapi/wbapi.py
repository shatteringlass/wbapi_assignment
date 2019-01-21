import requests
from .models import Country, Region, ILevel, LType


class WBAPIClient:

    COUNTRY_API_URL = "http://api.worldbank.org/v2/country"
    GEP_CSV_URL = "http://databank.worldbank.org/data/download/GEP_CSV.zip"

    def __init__(self):
        self.session = requests.Session()

    def base_request(self, url):
        response = self.session.get(url, params={'format': 'json'})
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise e
        else:
            return response.json()

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

    def all_countries(self):
        pass

    def get_country(self, country):
        url = f"{self.COUNTRY_API_URL}/{country}"
        response = self.base_request(url=url)
        country_json = None
        if len(response) == 1:
            # no result was returned
            raise Exception("The provided country code value is not valid.")
        else:
            country_json = response[1][0]
        return self.parse_country(country_json)
