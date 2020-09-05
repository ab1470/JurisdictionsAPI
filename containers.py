from dependency_injector import providers, containers
from data_manager import FirebaseClient
from services.nominatim import Nominatim
from add_data_view import AddDataView


class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')


class Clients(containers.DeclarativeContainer):
    firebase_client = providers.Singleton(FirebaseClient, Configs.config.firebase_admin_key_file)
    nominatim = Nominatim()


class Views(containers.DeclarativeContainer):
    add_data_view = providers.Factory(AddDataView, Clients.firebase_client, Clients.nominatim)
