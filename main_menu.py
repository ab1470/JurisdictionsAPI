from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import prompt, Separator
from examples import custom_style_2
from enum import Enum


class Options(Enum):
    ADD = 'Add new data'
    MODIFY = 'Modify existing data'
    DELETE = 'Delete data'
    EXIT = 'Exit'


qe = [
    {
        'type': 'list',
        'name': 'initial_action',
        'message': 'What do you want to do?',
        'choices': [
            Options.ADD.value,
            Options.MODIFY.value,
            Options.DELETE.value,
            Separator(),
            Options.EXIT.value
        ],
    }
]


class MainMenu:
    @staticmethod
    def show():
        initial_action = prompt(qe, style=custom_style_2)
        return initial_action
