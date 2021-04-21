#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
config.py contains all the global settings/configurations for the application.
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Redis URI

    REDIS_URI = 'redis://localhost'

    # Plivo Configurations

    PLIVO_AUTH_ID = 'YOUR_AUTH_ID'
    PLIVO_AUTH_TOKEN = 'YOUR_AUTH_TOKEN'
    PLIVO_NUMBER = 'SOURCE_NUMBER'
    PHLO_ID = 'PHLO_ID'