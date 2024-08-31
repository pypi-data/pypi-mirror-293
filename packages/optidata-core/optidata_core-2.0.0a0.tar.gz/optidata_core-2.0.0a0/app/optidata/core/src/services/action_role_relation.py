import logging

from ..database.mongo_collections import MONGO_COLLECTION_ACTION_ROLE_RELATIONS
from ..database.mongodb import MongoAPI
from ..utility.utils import get_message_error

log = logging.getLogger(__name__)


def new_action_role_relation(data):
    try:
        data = {
            'collection': MONGO_COLLECTION_ACTION_ROLE_RELATIONS,
            'Document': {
                'id_action': data.get('id_action'),
                'id_role': data.get('id_role')
            },
            'Filter': {
                'id_action': data.get('id_action'),
                'id_role': data.get('id_role')
            }
        }

        mongodb = MongoAPI(data)
        response = mongodb.write(data)

    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def get_all_action_role_relations_from_role(role_id):
    try:
        data = {
            'collection': MONGO_COLLECTION_ACTION_ROLE_RELATIONS,
            'Filter': {
                'id_role': role_id,
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.all()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response
