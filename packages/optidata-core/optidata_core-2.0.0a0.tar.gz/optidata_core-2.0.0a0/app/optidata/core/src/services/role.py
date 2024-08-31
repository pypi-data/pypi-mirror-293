import datetime
import logging

from bson import ObjectId

from ..database.mongo_collections import MONGO_COLLECTION_DATA_ROLES
from ..database.mongodb import MongoAPI
from ..utility.utils import get_message_error, get_datetime
from .action_role_relation import get_all_action_role_relations_from_role
from .action import get_action

log = logging.getLogger(__name__)


def new_role(data, is_admin=False, is_super_admin=False):
    try:
        date_doc = datetime.datetime.now()
        data = {
            'collection': MONGO_COLLECTION_DATA_ROLES,
            'Document': {
                'description': data.get('description'),
                'active': data.get('active'),
                'is_admin': is_admin,
                'is_super_admin': is_super_admin,
                'created_at': date_doc
            },
            'Filter': {
                'description': data.get('description')
            },
            'DataToBeUpdated': {
                'description': data.get('description'),
                'is_admin': is_admin,
                'is_super_admin': is_super_admin,
                'updated_at': date_doc
            }
        }

        mongodb = MongoAPI(data)
        response = mongodb.write(data)

    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def get_role(role_id):
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_ROLES,
            'Filter': {
                '_id': ObjectId(role_id)
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.read()

        action_role_relations = get_all_action_role_relations_from_role(role_id)
        actions = []
        for action_role_relation in action_role_relations:
            action = get_action(action_role_relation['id_action'])
            if len(action) > 0:
                actions.append(action[0])

        if len(response) > 0:
            response[0]["actions"] = actions

    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def get_all_roles():
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_ROLES,
            'Filter': {
                'active': True,
                'is_admin': False
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.all()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def update_role(pid: str, request):
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_ROLES,
            'Filter': {
                '_id': ObjectId(pid)
            },
            'DataToBeUpdated': {
                'description': request.get('description'),
                'updated_at': get_datetime()
            }
        }

        if 'active' in request:
            data['DataToBeUpdated'].update({'active': request.get('active')})

        mongodb = MongoAPI(data)
        response = mongodb.update()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def delete_role(pid: str):
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_ROLES,
            'Filter': {
                '_id': ObjectId(pid)
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.write(data)

        if response:
            data = {
                'collection': MONGO_COLLECTION_DATA_ROLES,
                'Filter': {
                    '_id': ObjectId(pid)
                },
                'DataToBeUpdated': {
                    'active': False,
                    'updated_at': get_datetime(),
                }
            }
            mongodb = MongoAPI(data)
            response = mongodb.update()
            if response:
                return {'Status': 'Eliminación exitosa'}

    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def check_role_exists(description):
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_ROLES,
            'Filter': {
                'description': description
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.read()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response
