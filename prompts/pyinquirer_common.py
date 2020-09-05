import platform
import os
from PyInquirer import prompt, Separator
from examples import custom_style_2
from data_models.geography_types import GeographyTypes

style = custom_style_2


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def erase_lines(count):
    for _ in range(count):
        print("\033[A                                                                                           \033[A")


class NavigationPrompt(object):
    main_menu = {
        'name': '[Return to the main menu]',
        'value': 'main_menu'
    }

    def __init__(self):
        self.choices = [self.main_menu]

    def _add_choice(self, choice, position=None):
        if position is not None:
            self.choices.insert(position, choice)
        else:
            self.choices.append(choice)

    def _make_questions(self):
        questions = {
            'type': 'list',
            'name': 'action',
            'message': 'Select an option',
            'choices': self.choices
        }

        return questions

    def _print_header(self):
        pass

    def ask(self):
        # self._print_header()
        questions = self._make_questions()
        answers = prompt(questions, style=style)
        return answers['action']


def select_from_list(objects):
    choices = []
    for index, obj in enumerate(objects):
        choices.append({'name': obj.name, 'value': index})

    question = [
        {
            'type': 'list',
            'name': 'list_options',
            'message': 'Found multiple matching entries. Please select one from this list',
            'choices': choices
        },
    ]

    selection = prompt(question, style=style)
    return selection['list_options']


def confirm(item_name, parent_type, parent_name):
    question = [
        {
            'type': 'confirm',
            'name': 'confirm',
            'message': f'Do you want to add \'{item_name}\' to the {parent_type} \'{parent_name}\'',
        },
    ]
    confirmation = prompt(question, style=style)
    return confirmation['confirm']