import datetime
import logging

from ..database.mongo_collections import MONGO_COLLECTION_ACTIONS
from ..database.mongodb import MongoAPI
from ..utility.utils import get_message_error

log = logging.getLogger(__name__)


def new_action(data):
    try:
        date_doc = datetime.datetime.now()
        data = {
            'collection': MONGO_COLLECTION_ACTIONS,
            'Document': {
                'id_action': data.get('id_action'),
                'display_name': data.get('display_name'),
                'group': data.get('group'),
                'created_at': date_doc
            },
            'Filter': {
                'id_action': data.get('id_action')
            },
            'DataToBeUpdated': {
                'display_name': data.get('display_name'),
                'updated_at': date_doc
            }
        }

        mongodb = MongoAPI(data)
        response = mongodb.write(data)

    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def get_action(id_action):
    try:
        data = {
            'collection': MONGO_COLLECTION_ACTIONS,
            'Filter': {
                'id_action': str(id_action)
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.read()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def get_all_actions():
    try:
        data = {
            'collection': MONGO_COLLECTION_ACTIONS,
        }
        mongodb = MongoAPI(data)
        response = mongodb.all()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def get_all_actions_from_group(group):
    try:
        data = {
            'collection': MONGO_COLLECTION_ACTIONS,
            'Filter': {
                'group': group,
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.all()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response
