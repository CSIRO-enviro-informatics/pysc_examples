# -*- coding: utf-8 -*-
# ★ UTF-8 ★
"""
A collection of utility functions to share common functionality between the examples
"""

import datetime
import pysc.settings
import pysc.models


def datetime_to_iso(_d):
    return _d.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def datetime_from_iso(_d):
    return datetime.datetime.strptime(_d, "%Y-%m-%dT%H:%M:%S.%fZ")


def create_organisation(organisation_id, name):
    org = pysc.models.Organisation(organisation_id)
    org.name = name
    org = org.save()
    assert org is not None, "Organisation {:s} could not be created.".format(organisation_id)

def setup_sensorcloud_basic(username, password, endpoint, debug=False):
    pysc.settings.load({'username': username, 'password': password, 'endpoint': endpoint, 'DEBUG_MODE': debug})

def setup_sensorcloud_apikey(apikey, endpoint, debug=False):
    pysc.settings.load({'apikey': apikey, 'endpoint': endpoint, 'DEBUG_MODE': debug})
