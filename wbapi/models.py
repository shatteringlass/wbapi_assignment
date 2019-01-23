
class ILevel:

    def __init__(self, _id, iso2, value):
        self.id = _id
        self.iso2 = iso2
        self.value = value

    def __repr__(self):
        return str(self.__dict__)


class LType:

    def __init__(self, _id, iso2, value):
        self.id = _id
        self.iso2 = iso2
        self.value = value

    def __repr__(self):
        return str(self.__dict__)


class Region:

    def __init__(self, _id, iso2, value):
        self.id = _id
        self.iso2 = iso2
        self.value = value

    def __repr__(self):
        return str(self.__dict__)


class Country:

    """
    iso2: 3 letter ISO 3166-1 alpha-3 code
    iso3: 2 letter ISO 3166-1 alpha-2 code
    name: Name
    region: Region: ID, name and World Bank 2 letter code
    ilevel: Income Level: ID, name and World Bank 2 letter code
    ltype: Lending Type: ID, name and World Bank 2 letter code
    capital: Capital City
    lon: Longitude
    lat: Latitude
    """

    def __init__(self, iso3, iso2, name, region, ilevel, ltype, capital, lon, lat):
        self.iso3 = iso3
        self.iso2 = iso2
        self.name = name
        self.region = region
        self.ilevel = ilevel
        self.ltype = ltype
        self.reg_id = self.region.id
        self.ilevel_id = self.ilevel.id
        self.ltype_id = self.ltype.id
        self.capital = capital
        self.lon = 
        self.lat = lat

    def __repr__(self):
        return str(self.__dict__)
