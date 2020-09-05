from prompts.pyinquirer_common import *


class GeographicPrompt(NavigationPrompt):
    institutions = {
        'name': f'View institutions',
        'value': 'view_institutions'
    }

    laws = {
        'name': f'View laws',
        'value': 'view_laws'
    }

    def __init__(self):
        super().__init__()
        self._add_choice(self.institutions)
        self._add_choice(self.laws)


class CountryPrompt(GeographicPrompt):
    admin_areas = {
        'name': f'View administrative areas (AKA States, Provinces, etc)',
        'value': 'administrative_areas'
    }

    def __init__(self, country):
        super().__init__()
        self._country = country
        self._add_choice(self.admin_areas, 1)

    def _print_header(self):
        print(f'===== Current Country: {self._country.name} '.ljust(140, '='))
        # print(f"> ID: {self._country.fsid},  "
        #       f"OSM ID: {self._country.osm_id},  "
        #       f"GEOHASH: {self._country.geohash},  "
        #       f"HAS BBOX: {self._country.bbox is not None}")


class AdminAreaPrompt(GeographicPrompt):
    municipalities = {
        'name': f'View municipalities',
        'value': 'municipalities'
    }
    subadmin_areas = {
        'name': f'View sub-administrative areas (AKA counties, etc)',
        'value': 'subadmin_areas'
    }

    def __init__(self, admin_area):
        super().__init__()
        self._admin_area = admin_area
        self._add_choice(self.municipalities, 1)
        self._add_choice(self.subadmin_areas, 2)

    def _print_header(self):
        print(f'===== Current Administrative Area: {self._admin_area.name} '.ljust(140, '='))
        # print(f"> ID: {self._admin_area.fsid},  "
        #       f"OSM ID: {self._admin_area.osm_id},  "
        #       f"GEOHASH: {self._admin_area.geohash},  "
        #       f"HAS BBOX: {self._admin_area.bbox is not None}")


class MunicipalityPrompt(GeographicPrompt):
    def __init__(self, municipality):
        super().__init__()
        self._municipality = municipality

    def _print_header(self):
        print(f'===== Current Municipality: {self._municipality.name} '.ljust(140, '='))
        # print(f"> ID: {self._municipality.fsid},  "
        #       f"OSM ID: {self._municipality.osm_id},  "
        #       f"GEOHASH: {self._municipality.geohash},  "
        #       f"HAS BBOX: {self._municipality.bbox is not None}")


class SubadminAreaPrompt(GeographicPrompt):
    def __init__(self, sub_admin_area):
        super().__init__()
        self._sub_admin_area = sub_admin_area

    def _print_header(self):
        print(f'===== Current Sub-Administrative Area: {self._sub_admin_area.name} '.ljust(140, '='))
        # print(f"> ID: {self._sub_admin_area.fsid},  "
        #       f"OSM ID: {self._sub_admin_area.osm_id},  "
        #       f"GEOHASH: {self._sub_admin_area.geohash},  "
        #       f"HAS BBOX: {self._sub_admin_area.bbox is not None}")