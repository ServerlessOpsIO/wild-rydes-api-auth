#!/usr/bin/env python3
'''
API Key
'''

from datetime import datetime
import json
import secrets

TOKEN_BYTES = 32

ID = 'Id'
KEY = 'Key'
DATETIME = 'DateTime'
TTL = 'TTL'
ACTIVE = 'Active'

def _genrate_api_key(identity: str, secret: str) -> str:
    '''Generate an API key value'''
    return secrets.token_hex(32)


def create(identity: str) -> object:
    '''Create a new ApiKey object'''
    return ApiKey(identity, secrets.token_hex(TOKEN_BYTES))


def get_from_ddb_item(item: dict) -> object:
    '''Return an API ApiKey object based on a DDB item'''
    d = {
        'identity': item.get(ID),
        'key': item.get(KEY),
        'date_time': item.get(DATETIME),
        'ttl': item.get(TTL),
        'active': item.get(ACTIVE)
    }
    return ApiKey(**d)

class ApiKeyErrorBase(Exception):
    '''Base exception class'''
    def __init__(self, message, identity) -> None:
        message = 'API Key Id already exists'
        super().__init__(message)

        self.identity = identity

    def json(self) -> dict:
        '''Return error as JSON'''
        d = {
            'ErrorType': self.__class__.__name__,
            'ErrorMessage': self.message,
            "Id": self.identity
        }
        return json.dumps(d)

class ApiKeyExistsError(ApiKeyErrorBase):
    '''Key already exists'''
    def __init__(self, identity) -> None:
        message = "API key already exists"
        super().__init__(message)


class ApiKey:
    '''API key class'''
    def __init__(self, identity: str, key: str, date_time=None, active=True, ttl=0) -> None:
        self._identity = identity
        self._key = key
        self._active = active
        self._ttl = ttl
        if date_time:
            self._date_time = date_time
        else:
            self._date_time = datetime.utcnow()

    def get_ddb_item(self):
        '''Return representation of data as a DDB item.'''
        d = {
            ID: self.get_identity(),
            KEY: self.get_key(),
            DATETIME: self._get_date_time_timestamp(),
            ACTIVE: self.get_active(),
            TTL: self.get_ttl()
        }
        return d

    def _get_date_time_timestamp(self) -> int:
        '''Return date time as seconds since unix epoch'''
        return int(self.get_date_time().timestamp())

    def get_active(self) -> str:
        '''Return API key active'''
        return self._active

    def get_date_time(self) -> datetime:
        '''Return API datetime'''
        return self._date_time

    def get_identity(self) -> str:
        '''Return API key identity'''
        return self._identity

    def get_key(self) -> str:
        '''Return API key key'''
        return self._key

    def get_ttl(self) -> int:
        '''Return API key ttl'''
        return self._ttl

