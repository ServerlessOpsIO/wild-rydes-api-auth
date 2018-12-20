#!/usr/bin/env python3

'''
Author: Tom McLaughlin
Email: tom@serverlessops.io

Description: Logging utility functions.
'''

import logging
import os


def get_logger(name: str):
    '''Return a logger'''
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
    _logger = logging.getLogger(name)
    return _logger

