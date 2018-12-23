'''Update API key'''

import json

from lambda_decorators import dump_json_body, load_json_body, on_exception
from src import api_key, ddb, logging
from src.errors import apig_responder, ApiAuthSvcUpdateApiKeyFailedError

_logger = logging.get_logger(__name__)
DDT = ddb.DynamoDBTable()


def _get_id_from_event(event: dict) -> str:
    '''get ID from event'''
    pass


def _get_timestamp_from_event(event: dict) -> str:
    '''get ID from event'''
    pass


def _get_attribute_from_event(event: dict) -> str:
    '''get ID from event'''
    pass


def _update_key_ttl(keyid: str, ttl: int) -> None:
    '''Update key TTL'''
    pass


def _update_key_active(keyid: str) -> None:
    '''Make key active'''
    pass


def _update_key_inactive(keyid: str) -> None:
    '''Update key TTL'''
    pass


@load_json_body
@dump_json_body
@on_exception(lambda e: apig_responder(e))
def handler(event, context):
    '''Function entry'''
    _logger.info('Event: {}'.format(json.dumps(event)))

    resp = {
        'statusCode': 201,
        'body': {'Status': 'NOOP'}
    }

    # XXX: Make sure to scrub API KEY.
    _logger.info('Response: {}'.format(json.dumps(resp)))
    return resp

