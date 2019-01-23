class GDPDatapoint:

    def __init__(self, ctry_name, ctry_code, year, value):
        self.ctry_name = ctry_name
        self.ctry_code = ctry_code
        self.year = year
        self.value = value

    def __repr__(self):
        return str(self.__dict__)


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
        self.lon = lon
        self.lat = lat

    def __repr__(self):
        return str(self.__dict__)
