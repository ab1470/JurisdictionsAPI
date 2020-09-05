from __future__ import print_function, unicode_literals
from data_models.geographic_area_model import GeographicArea
from data_models.country import Country
from data_models.administrative_area import AdministrativeArea
from data_models.geography_types import GeographyTypes
from data_manager import *


class GeographyTree:

    class GeoObject:
        obj: Country
        doc: DocumentSnapshot

        def __init__(self, obj, doc):
            self.obj = obj
            self.doc = doc

    country: GeoObject = None
    admin_area: GeoObject = None
    municipality: GeoObject = None
    subadmin_area: GeoObject = None

    def set_item(self, geo_type: GeographyTypes, obj: GeographicArea, doc: DocumentSnapshot):
        geo_object = GeographyTree.GeoObject(obj, doc)
        if geo_type is GeographyTypes.COUNTRY:
            self.country = geo_object
        elif geo_type is GeographyTypes.ADMINISTRATIVE_AREA:
            self.admin_area = geo_object
        elif geo_type is GeographyTypes.MUNICIPALITY:
            self.admin_area = geo_object
        elif geo_type is GeographyTypes.SUBADMIN_AREA:
            self.subadmin_area = geo_object

    def to_dict(self):
        dict = {}

        if self.country is not None:
            dict['countrycode'] = self.country.obj.country_code

        if self.admin_area is not None:
            dict['state'] = self.admin_area.obj.name

        # if self.SubAdminArea is not None:
        #     dict['county'] = self.SubAdminArea.obj.name
        #
        # if self.Municipality is not None:
        #     dict['city'] = self.Municipality.obj.name

        return dict

    def clear(self):
        pass
        # self.country = None
        # self.admin_area = None
        # self.subadmin_area = None
        # self.municipality = None

    def header_str(self, geo_type: GeographyTypes):
        geo_strings = []
        separator = ' > '

        def country_header_strings():
            return [self.country.obj.name]

        def admin_area_header_strings():
            geo_list = country_header_strings()
            geo_list.append(self.admin_area.obj.name)
            return geo_list

        def municipality_header_strings():
            geo_list = admin_area_header_strings()
            geo_list.append(self.municipality.obj.name)
            return geo_list

        def subadmin_area_header_strings():
            geo_list = admin_area_header_strings()
            geo_list.append(self.subadmin_area.obj.name)
            return geo_list

        if geo_type is GeographyTypes.COUNTRY:
            geo_strings = country_header_strings()
        elif geo_type is GeographyTypes.ADMINISTRATIVE_AREA:
            geo_strings = admin_area_header_strings()
        elif geo_type is GeographyTypes.MUNICIPALITY:
            geo_strings = municipality_header_strings()
        elif geo_type is GeographyTypes.SUBADMIN_AREA:
            geo_strings = subadmin_area_header_strings()

        return separator.join(geo_strings)


    # TODO: Delete this?
    # def print_header(self, geo_type: GeographyTypes):
    #     geo_strings = []
    #     separator = ' > '
    #
    #     def country_header_strings():
    #         return [self.country.obj.name]
    #
    #     def admin_area_header_strings():
    #         return country_header_strings().append(self.admin_area.obj.name)
    #
    #     def municipality_header_strings():
    #         return admin_area_header_strings().append(self.municipality.obj.name)
    #
    #     def subadmin_area_header_strings():
    #         return admin_area_header_strings().append(self.subadmin_area.obj.name)
    #
    #     if geo_type is GeographyTypes.COUNTRY:
    #         geo_strings = country_header_strings()
    #     elif geo_type is GeographyTypes.ADMINISTRATIVE_AREA:
    #         geo_strings = admin_area_header_strings()
    #     elif geo_type is GeographyTypes.MUNICIPALITY:
    #         geo_strings = municipality_header_strings()
    #     elif geo_type is GeographyTypes.SUBADMIN_AREA:
    #         geo_strings = subadmin_area_header_strings()
    #
    #     print(f'===== {separator.join(geo_strings)} '.ljust(140, '='))
