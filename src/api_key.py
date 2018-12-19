#!env python
'''
API Key
'''

import base64
import secrets

TOKEN_BYTES = 32


def _encode_api_key(identity: str, secret: str) -> bytes:
    """Encode API key value"""
    s = ':'.join([identity, secret])
    return base64.b64encode(s.encode())


def _decode_api_key(key: str) -> tuple:
    """Decode API key value"""
    key_bytes = key.encode()
    identity, secret = base64.b64decode(key_bytes).decode().split(':')
    return (identity, secret)


def create_api_key_obj(identity: str) -> object:
    '''Create a new ApiKey object'''
    return ApiKey(identity, secrets.token_hex(TOKEN_BYTES))


def get_api_key_obj_by_key(key: str) -> object:
    '''Get an ApiKey object by API key'''
    identity, secret = _decode_api_key(key)
    return ApiKey(identity, secret)


class ApiKey:
    """API key class"""
    def __init__(self, identity: str, secret: str):
        self._identity = identity
        self._secret = secret
        self._key = _encode_api_key(identity, secret)

    def get_identity(self) -> str:
        '''Return API key identity'''
        return self._identity

    def get_secret(self) -> str:
        '''Return API key secret'''
        return self._secret

    def get_key_string(self) -> str:
        '''Return API key'''
        return self._key.decode()

