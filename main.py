from __future__ import print_function, unicode_literals

from data_manager import FirebaseClient
from main_menu import MainMenu
from prompts.pyinquirer_common import clear

from containers import Views, Configs

def show_header():
    print("\n––------------------------------------------------------------------------------------------------")
    print("=== Jurisdictions API Manager ====================================================================")
    print("––------------------------------------------------------------------------------------------------\n")


def main():

    Configs.config.override({
        "firebase_admin_key_file": "./FirebaseAdminKey.json",
    })

    add_data_view = Views.add_data_view()

    show_header()
    fb_manager = FirebaseClient

    while True:
        action = MainMenu.show()['initial_action']

        if action == 'Exit':
            break

        if action == 'Add new data':
            clear()
            add_data_view.execute()

    # if action == MainMenu.EXIT.value:
    #     print("exiting...")
    #     exit(0)
    # elif action == MainMenu.ADD.value:
    #     print("adding...")
    #     stuff = fbMangager.get_stuff()
    #     print(stuff)
    # elif action == MainMenu.MODIFY.value:
    #     print("modifying...")
    # elif action == MainMenu.DELETE.value:
    #     print("deleting...")

    # print(answers['initial_action'])
    # pprint(action)


if __name__ == '__main__':
    main()
