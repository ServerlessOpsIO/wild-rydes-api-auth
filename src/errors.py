#!/usr/bin/env python3

'''
Author: Tom McLaughlin
Email: tom@serverlessops.io

Description: Service error classes.
'''

import json

class ApiAuthSvcBaseError(Exception):
    '''Base exception class'''


class ApiAuthSvcRequestError(ApiAuthSvcBaseError):
    '''Service Request error'''
    def __init__(self, message, identity) -> None:
        super().__init__(message)

        self.message = message
        self.identity = identity
        self.error_code = 500

    def get_json(self) -> dict:
        '''Return error as JSON'''
        d = {
            'ErrorType': self.__class__.__name__,
            'ErrorMessage': self.message,
            'Id': self.identity
        }
        return json.dumps(d)

    def get_apig_response(self) -> dict:
        '''Return a response suitable for API Gateway'''
        resp = {
            'statusCode': self.error_code,
            'body': self.get_json()
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


