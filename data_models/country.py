
from data_models.geographic_area_model import GeographicArea


class Country(GeographicArea):
    def __init__(self, fs_id, name: str = None, fs_dict: dict = None):
        super().__init__(fs_id, name, fs_dict)

        if fs_dict is not None:
            if 'country_code' in fs_dict.keys():
                self.country_code = fs_dict['country_code']
            if 'admin_area_title' in fs_dict.keys():
                self.admin_area_title = fs_dict['admin_area_title']

    country_code = None
    admin_area_title = None

    #
    # def to_dict(self):
    #     # ...

    # def to_prompt_options(self):
    #     options = ({'name': self.name, 'value': self.fsid})
    #     return options

    def __repr__(self):
        str = f'Country(NAME: {self.name},  FSID: {self.fsid}'
        if self.country_code is not None:
            str += f',  COUNTRY CODE: {self.country_code}'
        if self.osm_id is not None:
            str += f',  OSM ID: {self.osm_id}'
        if self.bbox is not None:
            str += f',  BBOX: {self.bbox}'
        if self.geohash is not None:
            str += f',  GEOHASH: {self.geohash}'
        if self.admin_area_title is not None:
            str += f',  ADMIN AREA TITLE: {self.admin_area_title}'
        str += ')'

        return str
