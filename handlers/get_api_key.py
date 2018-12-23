'''Get API keys'''

import json

from lambda_decorators import dump_json_body, load_json_body, on_exception
from src import api_key, ddb, logging
from src.errors import apig_responder, ApiAuthSvcGetApiKeyFailedError

_logger = logging.get_logger(__name__)
DDT = ddb.DynamoDBTable()


def _get_api_key(apik_id):
    '''Delete and API key.'''
    pass


def _get_api_key_by_timestamp(apik_id, timestamp):
    '''Delete and API key.'''
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

