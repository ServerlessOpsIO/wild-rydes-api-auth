'''Create API key'''

import json

from lambda_decorators import dump_json_body, load_json_body, on_exception
from src import api_key, ddb, logging
from src.errors import ApiAuthSvcDuplicateApiKeyError, ApiAuthSvcCreateApiKeyFailedError, ApiAuthSvcInvalidRequestData

_logger = logging.get_logger(__name__)
DDT = ddb.DynamoDBTable()


def _get_api_key_id_from_event(event: dict) -> str:
    '''Get the API key identity from the event'''
    try:
        ident = event['body'].get(DDT.hash_key)
    except Exception as e:
        _logger.exception(e)
        raise ApiAuthSvcInvalidRequestData
    return ident


def _check_key_exists(apik_id: str) -> bool:
    '''check if ApiKey Id already exists'''
    # XXX: this is only meant for creating new keys. If you're creating a key
    # and it already exists then I want you to know that. Maybe you don't need
    # another key? I'm not worried about leaking the existence, or lack of, a
    # key because because that's no important to us.
    try:
        return DDT.check_item_exists(apik_id)
    except Exception as e:
        _logger.info(e)
        raise ApiAuthSvcCreateApiKeyFailedError()


def _create_api_key(apik_id) -> dict:
    '''Create API key in DDB'''
    try:
        apik = api_key.create(apik_id)
        apkik_ddb_item = apik.get_ddb_item()
        _write_key_to_ddb(apkik_ddb_item)
    except Exception as e:
        _logger.exception(e)
        raise ApiAuthSvcCreateApiKeyFailedError(apik_id)

    return apkik_ddb_item


def _write_key_to_ddb(apik: dict) -> None:
    '''Write ApiKey object top DDB'''
    DDT.put_item(apik)


@load_json_body
@dump_json_body
@on_exception(lambda e: e.get_apig_response())
def handler(event, context):
    '''Function entry'''
    _logger.info('Event: {}'.format(json.dumps(event)))

    api_key_id = _get_api_key_id_from_event(event)

    if _check_key_exists(api_key_id):
        raise ApiAuthSvcDuplicateApiKeyError(api_key_id)

    apkik_ddb_item = _create_api_key(api_key_id)

    resp = {
        'statusCode': 201,
        'body': apkik_ddb_item
    }

    # XXX: Make sure to scrub API KEY.
    _logger.info('Response: {}'.format(json.dumps(resp)))
    return resp

