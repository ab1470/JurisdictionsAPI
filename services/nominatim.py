import requests
from enum import Enum
from data_models.country import *
from data_models.administrative_area import *
from data_models.municipality import *
from data_models.sub_admin_area import *


class SearchType(Enum):
    COUNTRY = 'country'
    STATE = 'state'
    COUNTY = 'county'
    CITY = 'city'


def create_geo_objects_from(content, searchtype: SearchType):
    return [y for y in (create_geo_object_from(x, searchtype) for x in content['features']) if y is not None]


def create_geo_object_from(feature, searchtype: SearchType):
    if 'address' not in feature['properties'].keys():
        return

    address_dict = feature['properties']['address']

    if searchtype.value not in address_dict.keys():
        return

    if searchtype == SearchType.COUNTRY:
        if 'country_code' not in address_dict.keys():
            return
        fsid = address_dict['country_code']
    else:
        fsid = address_dict[searchtype.value].lower()

    name = address_dict[searchtype.value]

    geo_obj = _create_geo_obj_for_type(searchtype, name, fsid)

    # TODO: Store all address information in a map dict
    geo_obj.osm_id = feature['properties']['osm_id']
    geo_obj.bbox = feature['bbox']

    return geo_obj


def _create_geo_obj_for_type(searchtype: SearchType, name, fsid):
    if searchtype == SearchType.COUNTRY:
        country_obj = Country(fsid, name)
        country_obj.country_code = fsid
        return country_obj
    if searchtype == SearchType.STATE:
        return AdministrativeArea(fsid, name)
    if searchtype == SearchType.CITY:
        return Municipality(fsid, name)
    if searchtype == SearchType.COUNTY:
        return SubAdministrativeArea(fsid, name)


class Nominatim:
    def __init__(self, url='http://nominatim.openstreetmap.org'):
        self.url = url

    def search(self, query, searchtype: SearchType = None, geo_tree=None):
        print("SEARCHING")
        if searchtype is not None:
            searchparam = searchtype.value
        else:
            searchparam = 'q'

        payload = {
            'format': 'geojson',
            'accept-language': 'en_us',
            'addressdetails': 1,
            searchparam: query,
        }
        if geo_tree is not None:
            if 'countrycode' in geo_tree.keys():
                payload['countrycodes'] = geo_tree['countrycode']
            if 'state' in geo_tree.keys():
                payload['state'] = geo_tree['state']
            if 'county' in geo_tree.keys():
                payload['county'] = geo_tree['county']
            if 'city' in geo_tree.keys():
                payload['city'] = geo_tree['city']

        r = requests.get(self.url, params=payload)
        content = r.json()

        results = create_geo_objects_from(content, searchtype)
        return results

    # def get_city_from_geohash(self, geohash):
    #     lat, lon = geohash_decode(geohash)
    #
    #     return self.get_city_from_point(lat, lon)

    # def get_country_from_point(self, lat, lon):
    #     payload = {
    #         'format': 'json',
    #         'accept-language': 'en_us,en,fr',
    #         'lat': lat,
    #         'lon': lon,
    #     }
    #     r = requests.get(self.url + '/reverse', params=payload)
    #     content = r.json()
    #     country_code = content['address']['country_code']
    #     country_name = content['address']['country']
    #
    #     return self.get_country_from_name(country_name, country_code)
    #
    # def get_city_from_point(self, lat, lon):
    #     payload = {
    #         'format': 'json',
    #         'accept-language': 'en_us,en,fr',
    #         'lat': lat,
    #         'lon': lon,
    #     }
    #     r = requests.get(self.url + '/reverse', params=payload)
    #     content = r.json()
    #
    #     county = ''
    #
    #     if 'county' in content['address']:
    #         county = content['address']['county']
    #
    #     if 'village' in content['address']:
    #         city_name = content['address']['village']
    #     elif 'town' in content['address']:
    #         city_name = content['address']['town']
    #     else:
    #         city_name = content['address']['city']
    #
    #     print '-----------extracted-city-name--------------'
    #     print city_name
    #
    #     country_code = content['address']['country_code']
    #
    #     if county != '':
    #         return self.get_city_from_name(city_name, country_code, county)
    #     else:
    #         return self.get_city_from_name(city_name, country_code)
    #
    # def _get_city(self, cities):
    #     for city in cities:
    #         if city['geojson']['type'] == 'Point':
    #             continue
    #
    #         if city['type'] == 'city':
    #             return city
    #
    #         if city['type'] == 'administrative':
    #             return city
    #
    #         if city['type'] == 'residential':
    #             return city
    #
    #     return cities
    #
    # def get_country_from_name(self, country_name, country_code):
    #     payload = {
    #         'countrycodes': country_code,
    #         'country': country_name,
    #         'format': 'json',
    #         'limit': 10,
    #         'polygon_geojson': 1,
    #     }
    #
    #     r = requests.get(self.url + '/search', params=payload)
    #     content = self._get_city(r.json())
    #
    #     country = Country()
    #     country.set_place_id(content['place_id'])
    #     country.set_centroid(content['lat'], content['lon'])
    #     country.set_geometry({
    #         "type": "FeatureCollection",
    #         "features": [
    #             {
    #                 "type": "Feature",
    #                 "properties": {},
    #                 "geometry": content['geojson']
    #             }
    #         ]
    #     })
    #
    #     return country
    #
    # def get_city_from_name(self, city_name, country_code, county_name=''):
    #     payload = {
    #         'city': city_name,
    #         'countrycodes': country_code,
    #         'format': 'json',
    #         'limit': 10,
    #         'polygon_geojson': 1,
    #     }
    #
    #     if county_name != '':
    #         payload['county'] = county_name
    #
    #     r = requests.get(self.url + '/search', params=payload)
    #     content = self._get_city(r.json())
    #
    #     city = City()
    #     city.set_place_id(content['place_id'])
    #     city.set_centroid(content['lat'], content['lon'])
    #     city.set_geometry({
    #         "type": "FeatureCollection",
    #         "features": [
    #             {
    #                 "type": "Feature",
    #                 "properties": {},
    #                 "geometry": content['geojson']
    #             }
    #         ]
    #     })
    #
    #     return city
