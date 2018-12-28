'''Check authorization token'''

import json

from boto3 import client
from lambda_decorators import dump_json_body, load_json_body, on_exception
from src import ddb, logging

_logger = logging.get_logger(__name__)
DDT = ddb.DynamoDBTable()
APIG = client('apigateway')

# Policy actions
DENY = 'Deny'
ALLOW = 'Allow'


def _on_exception(e: Exception) -> dict:
    '''Do on function exception'''
    _logger.exception(e)
    return _create_policy('*', DENY)

def _create_policy(arn: str, effect: str) -> dict:
    '''Create a policy ton return'''
    policy = {}
    policy['principalId'] = 'service'

    policy_doc = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'FirstStatement',
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': arn
            }
        ]
    }

    policy['policyDocument'] = policy_doc

    return policy

def _check_authorization_token_event(event: dict) -> bool:
    '''Check the authorization token in the event'''
    auth_token = event.get('authorizationToken')
    method_arn = event.get('methodArn')

    rest_id = _get_rest_id_from_arn(method_arn)
    apig_name = _get_apig_name_from_rest_id(rest_id)
    api_keys = _get_api_keys(apig_name)

    if auth_token in api_keys:
        effect = ALLOW
    else:
        effect = DENY

    return _create_policy(method_arn, effect)


def _get_api_keys(apig_name: str) -> list:
    '''Get list of API keys'''
    resp = DDT.query_by_item_id(apig_name)
    api_keys = []
    for key in resp:
        if key.get('Active', False):
            api_keys.append(key.get('Key'))
    return api_keys


def _get_apig_name_from_rest_id(rest_id: str) -> str:
    '''return APIG name from REST ID'''
    return APIG.get_rest_api(restApiId=rest_id).get('name')


def _get_rest_id_from_arn(arn: str) -> str:
    '''Get the APIG restId from the given ARN'''
    return arn.split(':')[-1].split('/')[0]


@load_json_body
@dump_json_body
@on_exception(lambda e: _on_exception(e))
def handler(event, context):
    '''Function entry'''
    _logger.info('Event: {}'.format(json.dumps(event)))

    policy = _check_authorization_token_event(event)

    # XXX: Make sure to scrub API KEY.
    _logger.info('Response: {}'.format(json.dumps(policy)))
    return policy


