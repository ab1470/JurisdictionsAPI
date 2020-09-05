from __future__ import print_function, unicode_literals
from prompts.geography_nav_prompts import *
from prompts.collection_nav_prompts import *
from prompts.geography_add_prompts import *
from navigation.geography_tree import *
from data_models.geography_types import GeographyTypes
from data_models.country import Country
from data_models.administrative_area import AdministrativeArea
from data_models.municipality import Municipality
from data_manager import *
import time


# FIXME: where does this belong?
def print_header(geography=None, menu=None):
    clear()
    header_str = ""
    if geography is not None:
        header_str = f" {geography} "
        if menu is not None:
            header_str += f"> {menu} "
    elif menu is not None:
        header_str = f" {menu} "
    print(f'====={header_str}'.ljust(140, '='))


def collection_to_countries(collection):
    return list(map(lambda x: Country(x.id, None, x.to_dict()), collection))


def collection_to_admin_areas(collection):
    return list(map(lambda x: AdministrativeArea(x.id, None, x.to_dict()), collection))


def collection_to_municipalities(collection):
    return list(map(lambda x: Municipality(x.id, None, x.to_dict()), collection))


class Menu:
    main_menu = "main_menu"
    countries = "countries"

    class Countries:
        item = "country"
        add = "add"

        class Country:
            admin_areas = "administrative_areas"
            institutions = "institutions"
            laws = "laws"

            class AdminAreas:
                item = "administrative_area"
                add = "add"

                class AdminArea:
                    municipalities = "municipalities"
                    subadmin_areas = "subadmin_areas"
                    institutions = "institutions"
                    laws = "laws"

                    class Municipalities:
                        item = "municipality"
                        add = "add"

                        class Municipality:
                            institutions = "institutions"
                            laws = "laws"

                    class SubadminAreas:
                        item = "subadmin_area"
                        add = "add"

                        class SudadminArea:
                            institutions = "institutions"
                            laws = "laws"

class AddDataView:
    fb_manager: FirebaseClient
    geography_tree = GeographyTree()
    nav_position = None

    def __init__(self, firebase_client, nominatim):
        self.fb_manager = firebase_client
        self.nominatim = nominatim

    def select_geography(self, geo_type: GeographyTypes):
        prompt = None
        collection = None
        geography_list = None
        next_menu = None

        if geo_type is GeographyTypes.COUNTRY:
            collection = self.fb_manager.get_countries()
            geography_list = collection_to_countries(collection)
            prompt = GeographyCollectionPrompt(geography_list, GeographyTypes.COUNTRY)
            next_menu = Menu.Countries

        elif geo_type is GeographyTypes.ADMINISTRATIVE_AREA:
            selected_country_doc = self.geography_tree.country.doc
            collection = self.fb_manager.get_admin_areas(selected_country_doc)
            geography_list = collection_to_admin_areas(collection)
            prompt = GeographyCollectionPrompt(geography_list, GeographyTypes.ADMINISTRATIVE_AREA)
            next_menu = Menu.Countries.Country.AdminAreas

        elif geo_type is GeographyTypes.MUNICIPALITY:
            selected_admin_area_doc = self.geography_tree.admin_area.doc
            collection = self.fb_manager.get_municipalities(selected_admin_area_doc)
            geography_list = collection_to_municipalities(collection)
            prompt = GeographyCollectionPrompt(geography_list, GeographyTypes.MUNICIPALITY)
            next_menu = Menu.Countries.Country.AdminAreas.AdminArea.Municipalities

        elif geo_type is GeographyTypes.SUBADMIN_AREA:
            pass

        action = prompt.ask()
        if action == 'add':
            return next_menu.add
        elif action == 'main_menu':
            return Menu.main_menu
        else:
            geography = geography_list[action]
            geography_doc = collection[action]
            self.geography_tree.set_item(geo_type, geography, geography_doc)
            print(geography)
            return next_menu.item

    def add_geography(self, geo_type: GeographyTypes):
        prompt = None

        if geo_type is GeographyTypes.COUNTRY:
            prompt = AddCountryPrompt(self.nominatim)
        elif geo_type is GeographyTypes.ADMINISTRATIVE_AREA:
            admin_area_title = self.geography_tree.country.obj.admin_area_title
            prompt = AddAdminAreaPrompt(self.nominatim, admin_area_title, self.geography_tree.to_dict())
        elif geo_type is GeographyTypes.MUNICIPALITY:
            prompt = AddMunicipalityPrompt(self.nominatim, self.geography_tree.to_dict())
        elif geo_type is GeographyTypes.SUBADMIN_AREA:
            pass

        new_geography = prompt.ask()

        # TODO: store the new geography in the database!
        if new_geography is not None:
            print(f"Adding '{new_geography.name}' to the database...")
        else:
            print("No geography added. Returning to the main menu.")

        # TODO: Do I want to sleep here, or in `execute()`?
        time.sleep(2)

        # TODO: I think I should `return Menu.main_menu` here
        # return Menu.main_menu

    def country_action(self):
        country = self.geography_tree.country.obj
        country_prompt = CountryPrompt(country)
        country_action = country_prompt.ask()

        if country_action == 'administrative_areas':
            return Menu.Countries.Country.admin_areas
        elif country_action == 'institutions':
            return Menu.Countries.Country.institutions
        elif country_action == 'laws':
            return Menu.Countries.Country.laws
        else:
            return Menu.main_menu

    def admin_area_action(self):
        admin_area = self.geography_tree.admin_area.obj
        admin_area_prompt = AdminAreaPrompt(admin_area)
        admin_area_action = admin_area_prompt.ask()

        if admin_area_action == 'municipalities':
            return Menu.Countries.Country.AdminAreas.AdminArea.municipalities
        if admin_area_action == 'subadmin_areas':
            return Menu.Countries.Country.AdminAreas.AdminArea.subadmin_areas
        elif admin_area_action == 'institutions':
            return Menu.Countries.Country.AdminAreas.AdminArea.institutions
        elif admin_area_action == 'laws':
            return Menu.Countries.Country.AdminAreas.AdminArea.laws
        else:
            return Menu.main_menu

    def execute(self):
        self.nav_position = Menu.countries
        while self.nav_position is not Menu.main_menu:

            if self.nav_position == Menu.countries:
                print_header(None, "Countries")
                self.nav_position = self.select_geography(GeographyTypes.COUNTRY)

            if self.nav_position == Menu.Countries.add:
                print_header(None, "Add a new country")
                self.add_geography(GeographyTypes.COUNTRY)
                self.nav_position = Menu.main_menu

            if self.nav_position == Menu.Countries.item:
                print_header(self.geography_tree.header_str(GeographyTypes.COUNTRY))
                self.nav_position = self.country_action()

            if self.nav_position == Menu.Countries.Country.admin_areas:
                admin_areas_title = self.geography_tree.country.obj.admin_area_title.title() + "s"
                geography_str = self.geography_tree.header_str(GeographyTypes.COUNTRY)
                print_header(geography_str, admin_areas_title)
                self.nav_position = self.select_geography(GeographyTypes.ADMINISTRATIVE_AREA)

            if self.nav_position == Menu.Countries.Country.institutions:
                print("institutions placeholder")
                self.nav_position = Menu.main_menu

            if self.nav_position == Menu.Countries.Country.laws:
                print("laws placeholder")
                self.nav_position = Menu.main_menu

            if self.nav_position == Menu.Countries.Country.AdminAreas.add:
                self.add_geography(GeographyTypes.ADMINISTRATIVE_AREA)
                self.nav_position = Menu.main_menu

            if self.nav_position == Menu.Countries.Country.AdminAreas.item:
                geography_str = self.geography_tree.header_str(GeographyTypes.ADMINISTRATIVE_AREA)
                print_header(geography_str)
                self.nav_position = self.admin_area_action()

            if self.nav_position == Menu.Countries.Country.AdminAreas.AdminArea.municipalities:
                geography_str = self.geography_tree.header_str(GeographyTypes.ADMINISTRATIVE_AREA)
                print_header(geography_str, "Municipalities")
                self.nav_position = self.select_geography(GeographyTypes.MUNICIPALITY)

            if self.nav_position == Menu.Countries.Country.AdminAreas.AdminArea.Municipalities.add:
                self.add_geography(GeographyTypes.MUNICIPALITY)
                self.nav_position = Menu.main_menu

            if self.nav_position == Menu.Countries.Country.AdminAreas.AdminArea.Municipalities.item:
                pass
                # self.nav_position = self.

            if self.nav_position == Menu.Countries.Country.AdminAreas.AdminArea.subadmin_areas:
                pass

            if self.nav_position == Menu.Countries.Country.AdminAreas.AdminArea.SubadminAreas.add:
                pass
                # TODO: remove `pass`
                self.add_geography(GeographyTypes.SUBADMIN_AREA)
                self.nav_position = Menu.main_menu

            if self.nav_position == Menu.Countries.Country.AdminAreas.AdminArea.SubadminAreas.item:
                pass

            if self.nav_position == Menu.Countries.Country.AdminAreas.AdminArea.institutions:
                pass

            if self.nav_position == Menu.Countries.Country.AdminAreas.AdminArea.laws:
                pass

            # else:
            #     if country_action == 'administrative_areas':

            #         else:
            #             erase_lines(1)
            #             admin_area = admin_areas[admin_areas_action]
            #             self.geography_tree.append(admin_area.name)
            #             print(self.geography_tree)
            #             admin_area_prompt = AdminAreaPrompt(admin_area)
            #             admin_area_action = admin_area_prompt.ask()

        print("Returning to the main menu...")
        self.geography_tree.clear()
        time.sleep(1)
        clear()
        return
