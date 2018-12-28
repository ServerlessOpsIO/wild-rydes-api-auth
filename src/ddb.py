#!/usr/bin/env python3

'''
Author: Tom McLaughlin
Email: tom@serverlessops.io

Description: DynamoDB tables
'''
import os

import boto3
from boto3.dynamodb.conditions import Key
from .errors import ApiAuthSvcBaseError
from . import logging

_logger = logging.get_logger(__name__)

DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME', '')
DDB_HASH_KEY = os.environ.get('DDB_HASH_KEY', '')
DDB_RANGE_KEY = os.environ.get('DDB_RANGE_KEY', '')

class DynamoDBTableBaseError(Exception):
    '''Base exception class'''


class DynamoDBTableCheckItemError(DynamoDBTableBaseError):
    '''Error checking item existence in dynamoDB'''
    msg = "Error checking item existence in DynamoDB"
    def __init__(self, message=msg) -> None:
        super().__init__(message)


class DynamoDBTableGetItemError(DynamoDBTableBaseError):
    '''Error Getting item in dynamoDB'''
    msg = "Unable to get item from DynamoDB"
    def __init__(self, message=msg) -> None:
        super().__init__(message)


class DynamoDBTablePutItemError(DynamoDBTableBaseError):
    '''Error Putting item in dynamoDB'''
    msg = "Unable to write item to DynamoDB"
    def __init__(self, message=msg) -> None:
        super().__init__(message)


class DynamoDBTableQueryItemError(DynamoDBTableBaseError):
    '''Error querying item in dynamoDB'''
    msg = "Unable to query item in DynamoDB"
    def __init__(self, message=msg) -> None:
        super().__init__(message)


class DynamoDBTable:
    '''DynamoDB Table'''
    def __init__(self, table_name: str = DDB_TABLE_NAME, hash_key: str = DDB_HASH_KEY, range_key: str = DDB_RANGE_KEY) -> None:
        self._table_name = table_name
        self._hash_key = hash_key
        self._range_key = range_key
        self._ddb_resoruce = boto3.resource('dynamodb')
        self._ddb_table = self._ddb_resoruce.Table(self._table_name)

    @property
    def table_name(self) -> str:
        '''DDB table name.'''
        return self._table_name

    @property
    def hash_key(self) -> str:
        '''DDB table hash key'''
        return self._hash_key

    @property
    def range_key(self) -> str:
        '''DDB table range key'''
        return self._range_key

    def check_item_exists(self, item_id) -> bool:
        '''Check if item already exists'''
        try:
            resp = self._ddb_table.query(
                Select='COUNT',
                KeyConditionExpression=Key(self._hash_key).eq(item_id)
            )
        except Exception as e:
            _logger.exception(e)
            raise DynamoDBTableCheckItemError

        return resp.get('Count') > 0

    def get_item(self, item_id, range_value, consistent_read=False) -> dict:
        '''Return an item'''
        _logger.info(item_id)
        try:
            items = self._ddb_table.get_item(
                Key={
                    self._hash_key: item_id,
                    self._range_key: range_value
                },
                ConsistentRead=consistent_read
            )
        except Exception as e:
            _logger.exception(e)
            raise DynamoDBTableGetItemError
        return items.get('Items')


    def put_item(self, item: dict) -> None:
        '''Put item in DDB'''
        try:
            self._ddb_table.put_item(
                Item=item
            )
        except Exception as e:
            _logger.exception(e)
            raise DynamoDBTablePutItemError

    def query_by_item_id(self, item_id, start_key: dict = {}) -> list:
        '''query for item'''
        item_list = []

        query_kwargs = {
            'KeyConditionExpression': Key(self._hash_key).eq(item_id)
        }

        if bool(start_key):
            query_kwargs['ExclusiveStartKey'] = start_key

        try:
            resp = self._ddb_table.query(**query_kwargs)
        except Exception as e:
            _logger.exception(e)
            raise DynamoDBTableQueryItemError

        item_list += resp.get('Items')

        if bool(resp.get('LastEvaluatedKey')):
            item_list += self.query_by_item_id(item_id, resp.get('LastEvaluatedKey'))

        return item_list

