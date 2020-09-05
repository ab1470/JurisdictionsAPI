from prompts.pyinquirer_common import *
from enum import Enum


class CollectionPrompt(NavigationPrompt):
    class Options(Enum):
        ADD = 'add'

    def _add_new_prompt(self, item_name):
        return {
            'name': f'[Add a new {item_name}]',
            'value': self.Options.ADD.value
        }

    def __init__(self, collection_name, item_name, document_objects):
        super().__init__()
        self._item_name = item_name
        self._collection_name = collection_name
        add_prompt = self._add_new_prompt(item_name)
        self._add_choice(add_prompt, 1)
        self.add_collection_choices(document_objects)

    def add_collection_choices(self, document_objects):
        for index, obj in enumerate(document_objects):
            choice = {'name': obj.name, 'value': index}
            self._add_choice(choice)

    def _print_header(self):
        print(f'===== Current Collection: {self._collection_name} '.ljust(140, '='))


class GeographyCollectionPrompt(CollectionPrompt):
    def __init__(self, document_objects, geo_type: GeographyTypes):
        if geo_type is GeographyTypes.COUNTRY:
            super().__init__('Countries', 'country', document_objects)
        elif geo_type is GeographyTypes.ADMINISTRATIVE_AREA:
            super().__init__('Administrative Areas', 'administrative area', document_objects)
        elif geo_type is GeographyTypes.MUNICIPALITY:
            super().__init__('Municipalities', 'municipality', document_objects)
        elif geo_type is GeographyTypes.SUBADMIN_AREA:
            super().__init__('Sub-administrative Areas', 'sub-administrative area', document_objects)
