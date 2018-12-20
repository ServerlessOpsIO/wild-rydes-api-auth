#!/usr/bin/env python3

'''
Author: Tom McLaughlin
Email: tom@serverlessops.io

Description: API Keys
'''

from datetime import datetime
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


class ApiKey:
    '''API key class'''
    def __init__(self, identity: str, key: str, date_time = None, active: bool = True, ttl=0) -> None:
        self._identity = identity
        self._key = key
        self._active = active
        self._ttl = ttl
        if date_time:
            self._date_time = date_time
        else:
            self._date_time = datetime.utcnow()

    def _get_date_time_timestamp(self) -> int:
        '''Return date time as seconds since unix epoch'''
        return int(self.date_time.timestamp())

    @property
    def active(self) -> str:
        '''Return API key active'''
        return self._active

    @property
    def date_time(self) -> datetime:
        '''Return API datetime'''
        return self._date_time

    @property
    def identity(self) -> str:
        '''Return API key identity'''
        return self._identity

    @property
    def key(self) -> str:
        '''Return API key key'''
        return self._key

    @property
    def ttl(self) -> int:
        '''Return API key ttl'''
        return self._ttl

    def get_ddb_item(self):
        '''Return representation of data as a DDB item.'''
        d = {
            ID: self.identity,
            KEY: self.key,
            DATETIME: self._get_date_time_timestamp(),
            ACTIVE: self.active,
            TTL: self.ttl
        }
        return d

