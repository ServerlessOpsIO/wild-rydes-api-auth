#!/usr/bin/env python3

'''
Author: Tom McLaughlin
Email: tom@serverlessops.io

Description: Service error classes.
'''

import json
from src import logging
_logger = logging.get_logger(__name__)


def apig_responder(e):
    '''helper function for responding to APIG when errors occur'''
    _logger.exception(e)
    if hasattr(e, 'get_apig_response'):
        return e.get_apig_response()
    return ApiAuthSvcRequestError('Error servicing request', None).get_apig_response()


class ApiAuthSvcBaseError(Exception):
    '''Base exception class'''
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message

    def get_dict(self) -> dict:
        '''return error dictionary'''
        d = {
            'ErrorType': self.__class__.__name__,
            'ErrorMessage': self.message,
        }
        return d

    def get_json(self) -> str:
        '''Return error as JSON'''
        d = self.get_dict()
        return json.dumps(d)


class ApiAuthSvcRequestError(ApiAuthSvcBaseError):
    '''Service Request error'''
    def __init__(self, message, identity) -> None:
        super().__init__(message)

        self.identity = identity
        self.error_code = 500

    def get_dict(self) -> dict:
        '''return error dictionary'''
        d = super().get_dict()
        d['Id'] = self.identity
        return d

    def get_apig_response(self) -> dict:
        '''Return a response suitable for API Gateway'''
        # We use get_dict() and not get_json() because we have a decorator
        # that will serialize this for us.
        resp = {
            'statusCode': self.error_code,
            'body': self.get_dict()
        }
        return resp


class ApiAuthSvcInvalidRequestData(ApiAuthSvcRequestError):
    '''Request contains invalid request data'''
    def __init__(self) -> None:
        message = "Request data invalid"
        super().__init__(message, None)


class ApiAuthSvcDuplicateApiKeyError(ApiAuthSvcRequestError):
    '''Key already exists'''
    def __init__(self, identity=None) -> None:
        message = "API key already exists"
        super().__init__(message, identity)


class ApiAuthSvcApiKeyDoesNotExistError(ApiAuthSvcRequestError):
    '''Key create failed'''
    def __init__(self, identity=None) -> None:
        message = "API key does not exist"
        super().__init__(message, identity)


class ApiAuthSvcCreateApiKeyFailedError(ApiAuthSvcRequestError):
    '''Key create failed'''
    def __init__(self, identity=None) -> None:
        message = "API key create failed"
        super().__init__(message, identity)


class ApiAuthSvcGetApiKeyFailedError(ApiAuthSvcRequestError):
    '''Key get failed'''
    def __init__(self, identity=None) -> None:
        message = "API key get failed"
        super().__init__(message, identity)


class ApiAuthSvcUpdateApiKeyFailedError(ApiAuthSvcRequestError):
    '''Key update failed'''
    def __init__(self, identity=None) -> None:
        message = "API key update failed"
        super().__init__(message, identity)


class ApiAuthSvcDeleteApiKeyFailedError(ApiAuthSvcRequestError):
    '''Key delete failed'''
    def __init__(self, identity=None) -> None:
        message = "API key delete failed"
        super().__init__(message, identity)


