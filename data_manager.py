import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.document import *


class FirebaseClient(object):
    def __init__(self, credentials_filepath):
        cred = credentials.Certificate(credentials_filepath)
        default_app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_collection(self, name, from_doc=None):
        if from_doc is not None:
            return from_doc.collection(f'{name}')
        else:
            return self.db.collection(f'{name}')

    def get_document(self, name, from_collection):
        return from_collection.document(f'{name}')

    def get_countries(self):
        return list(self.get_collection("countries").stream())

    # TODO: I think this isn't being used
    def get_location(self, country, admin_area=None, subadmin_area=None):
        ref = self.db.collection(u'countries').document(f'{country}')
        if admin_area is not None:
            ref = ref.collection(u'administrative_areas').document(f'{admin_area}')

            if subadmin_area is not None:
                ref = ref.collection(u'subadministrative_areas').document(f'{subadmin_area}')

        return ref.get()

    # TODO: abstract this code into a common method
    def get_admin_areas(self, country_doc):
        if type(country_doc) == DocumentSnapshot:
            doc_ref = country_doc.reference
            return list(self.get_collection('administrative_areas', doc_ref).stream())
        elif type(country_doc) == DocumentReference:
            return list(self.get_collection('administrative_areas', country_doc).stream())
        else:
            return

    # TODO: abstract this code into a common method
    def get_municipalities(self, admin_area_doc):
        if type(admin_area_doc) == DocumentSnapshot:
            doc_ref = admin_area_doc.reference
            return list(self.get_collection('municipalities', doc_ref).stream())
        elif type(admin_area_doc) == DocumentReference:
            return list(self.get_collection('municipalities', admin_area_doc).stream())
        else:
            return
