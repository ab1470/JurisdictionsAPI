
from data_models.geographic_area_model import GeographicArea

# TODO: this is almost identical to Municipality() and Country(). Abstract this and all similar classes.
class AdministrativeArea(GeographicArea):
    def __init__(self, fs_id, name: str = None, fs_dict: dict = None):
        super().__init__(fs_id, name, fs_dict)

        if fs_dict is not None:
            if 'laws' in fs_dict.keys():
                self.laws = fs_dict['laws']
            if 'institutions' in fs_dict.keys():
                self.institutions = fs_dict['institutions']

    laws = None
    institutions = None

    #
    # def to_dict(self):
    #     # ...

    # def to_prompt_options(self):
    #     options = ({'name': self.name, 'value': self.fsid})
    #     return options

    def __repr__(self):
        str = f'AdministrativeArea(NAME: {self.name},  FSID: {self.fsid}'
        if self.osm_id is not None:
            str += f',  OSM ID: {self.osm_id}'
        if self.bbox is not None:
            str += f',  BBOX: {self.bbox}'
        if self.geohash is not None:
            str += f',  GEOHASH: {self.geohash}'
        str += ')'

        return str
