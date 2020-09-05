
class GeographicArea(object):
    def __init__(self, fs_id, name: str = None, fs_dict: dict = None):
        self.fsid = fs_id
        self.name = name

        if fs_dict is not None:
            self.name = fs_dict['name']
            if 'osm_id' in fs_dict.keys():
                self.osm_id = fs_dict['osm_id']
            if 'bbox' in fs_dict.keys():
                self.bbox = fs_dict['bbox']
            if 'geohash' in fs_dict.keys():
                self.geohash = fs_dict['geohash']

    osm_id = None
    bbox = None
    geohash = None

    def to_dict(self):
        pass

    # def to_prompt_options(self):
    #     options = ({'name': self.name, 'value': self.fsid})
    #     return options

    def __repr__(self):
        str = f'GeographicArea(NAME: {self.name},  FSID: {self.fsid}'
        if self.osm_id is not None:
            str += f',  OSM ID: {self.osm_id}'
        if self.bbox is not None:
            str += f',  BBOX: {self.bbox}'
        if self.geohash is not None:
            str += f',  GEOHASH: {self.geohash}'
        str += ')'

        return str
