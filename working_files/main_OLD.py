import json

import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud.exceptions

cred = credentials.Certificate('./FirebaseAdminKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# sample_json = """
# {
#     "city": "Chicago",
#     "county": "Cook"
# }
# """
#
# sample = json.loads(sample_json)
# sample_city = sample["city"]
# sample_county = sample["county"]
#
# doc_ref = db.collection(u'states').document(u'illinois')
# doc_ref.set({
#     u'city': sample_city,
#     u'county': sample_county,
# })

illinois_ref = db.collection(u'countries').document(u'usa')\
    .collection(u'administrative_areas').document(u'illinois')

cook_cty_ref = illinois_ref\
    .collection(u'subadministrative_areas').document(u'cook')

chicago_ref = illinois_ref\
    .collection(u'localities').document(u'chicago')

cook_cty_ref.set({
    u'name': "Cook",
})

chicago_ref.set({
    u'name': "Chicago",
    u'counties': [cook_cty_ref]
})



new_york_ref = db.collection(u'countries').document(u'usa')\
    .collection(u'administrative_areas').document(u'new york')

new_york_cty_ref = new_york_ref\
    .collection(u'subadministrative_areas').document(u'new york')

kings_cty_ref = new_york_ref\
    .collection(u'subadministrative_areas').document(u'kings')

new_york_ref = new_york_ref\
    .collection(u'localities').document(u'new york')

new_york_cty_ref.set({
    u'name': "New York",
})

kings_cty_ref.set({
    u'name': "Kings",
})

new_york_ref.set({
    u'name': "New York",
    u'counties': [new_york_cty_ref, kings_cty_ref]
})


# try:
#     doc = doc_ref.get()
#     if doc.exists:
#         print(u'Document data: {}'.format(doc.to_dict()))
#     else:
#         print(u'No such document!')
# except google.cloud.exceptions.NotFound:
#     print(u'No such document!')