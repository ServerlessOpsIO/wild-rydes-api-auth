'''Create API key'''

import json

from src import api_key, ddb, logging
from src.errors import ApiAuthSvcBaseError, ApiAuthSvcInvalidRequestData, ApiAuthSvcDuplicateApiKeyError, ApiAuthSvcCreateApiKeyFailedError

_logger = logging.get_logger(__name__)
DDT = ddb.DynamoDBTable()


def _get_api_key_id_from_event(event: dict) -> str:
    '''Get the API key identity from the event'''
    try:
        body = json.loads(event.get('body'))
        ident = body.get(DDT.hash_key)
    except Exception:
        raise ApiAuthSvcInvalidRequestData()
    return ident


def _check_key_exists(apik_id: str) -> bool:
    '''check if ApiKey Id already exists'''
    # XXX: this is only meant for creating new keys. If you're creating a key
    # and it already exists then I want you to know that. Maybe you don't need
    # another key? I'm not worried about leaking the existence, or lack of, a
    # key because because that's no important to us.
    return DDT.check_item_exists(apik_id)

def _write_key_to_ddb(apik: dict) -> None:
    '''Write ApiKey object top DDB'''
    DDT.put_item(apik)


def handler(event, context):
    '''Function entry'''
    _logger.info('Event: {}'.format(json.dumps(event)))

    try:
        api_key_id = _get_api_key_id_from_event(event)

        if not _check_key_exists(api_key_id):
            apik = api_key.create(api_key_id)
            apkik_ddb_item = apik.get_ddb_item()
            _write_key_to_ddb(apkik_ddb_item)
        else:
            raise ApiAuthSvcDuplicateApiKeyError(api_key_id)
    except ApiAuthSvcBaseError as e:
        _logger.exception(e)
        if hasattr(e, 'identity'):
            identity = e.identity
        else:
            identity = None
        return ApiAuthSvcCreateApiKeyFailedError(identity).get_apig_response()

    resp = {
        'statusCode': 201,
        'body': json.dumps(apkik_ddb_item)
    }

    # XXX: Make sure to scrub API KEY.
    _logger.info('Response: {}'.format(json.dumps(resp)))
    return resp

