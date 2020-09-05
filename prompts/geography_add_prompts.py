from prompts.pyinquirer_common import *
from services.nominatim import SearchType


class AddGeographyPrompt(object):
    def __init__(self, nominatim, geography_title):
        self._nominatim = nominatim
        self._geography_title = geography_title

    def _print_header(self):
        pass

    @staticmethod
    def _search_prompt(item_name):
        search_prompt = [
            {
                'type': 'input',
                'name': 'search_text',
                'message': f'Enter the {item_name} name',
            },
        ]

        search = prompt(search_prompt, style=style)
        query = search['search_text']
        return query

    def _perform_search(self, query, searchtype: SearchType = None, geography_tree: dict = None):
        geography = self._nominatim.search(query, searchtype, geography_tree)
        while len(geography) == 0:
            print(f'Unable to find a {self._geography_title} named \'{query}\'. Please try again.')
            query = self._search_prompt(self._geography_title)
            return self._perform_search(query, searchtype, geography_tree)

        selected_index = 0

        if len(geography) > 1:
            selected_index = select_from_list(geography)

        geography = geography[selected_index]
        return geography

    def ask(self):
        self._print_header()
        query = self._search_prompt(self._geography_title)
        geography = self._perform_search(query)
        return geography


class AddCountryPrompt(AddGeographyPrompt):
    def __init__(self, nominatim):
        super().__init__(nominatim, 'country')

    @staticmethod
    def _area_title_prompt(geography):
        area_title_prompt = [
            {
                'type': 'input',
                'name': 'area_title',
                'message': f"What does '{geography.name}' call its administrative areas? (ex. 'state', 'province', etc)",
            },
        ]
        area_title_prompt = prompt(area_title_prompt, style=style)
        area_title = area_title_prompt['area_title']
        return area_title

    def ask(self):
        # self._print_header()
        query = self._search_prompt(self._geography_title)
        country = self._perform_search(query, SearchType.COUNTRY)
        admin_area_title = self._area_title_prompt(country)
        country.admin_area_title = admin_area_title
        print(country)
        return country


class AddAdminAreaPrompt(AddGeographyPrompt):
    def __init__(self, nominatim, admin_area_title, geography_tree: dict):
        super().__init__(nominatim, admin_area_title)
        self._geogrpahy_tree = geography_tree

    @staticmethod
    def _area_title_prompt(geography):
        area_title_prompt = [
            {
                'type': 'input',
                'name': 'area_title',
                'message': f"What does '{geography.name}' call its sub-administrative areas? (ex. 'county', etc)",
            },
        ]
        area_title_prompt = prompt(area_title_prompt, style=style)
        area_title = area_title_prompt['area_title']
        return area_title

    def ask(self):
        self._print_header()
        query = self._search_prompt(self._geography_title)
        admin_area = self._perform_search(query, SearchType.STATE, self._geogrpahy_tree)
        subadmin_area_title = self._area_title_prompt(admin_area)
        admin_area.admin_area_title = subadmin_area_title
        print(admin_area)
        return admin_area


class AddMunicipalityPrompt(AddGeographyPrompt):
    def __init__(self, nominatim, geography_tree: dict):
        super().__init__(nominatim, 'municipality')
        self._geogrpahy_tree = geography_tree

    def ask(self):
        self._print_header()
        query = self._search_prompt(self._geography_title)
        admin_area = self._perform_search(query, SearchType.CITY, self._geogrpahy_tree)
        print(admin_area)
        return admin_area
