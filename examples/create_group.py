#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example of using `pysc` to login to a SensorCloud instance endpoint and create a new group within your
organisation.

Note, the `pysc` lib, (and by extension these examples) require python 3.4 or above. Preferably use python 3.5 for best
compatibility and performance. 3.6 _should_ work, but it is not tested.
"""
__author__ = "Ashley Sommer"
__copyright__ = "Copyright 2017, CSIRO Land and Water"

import logging
import sys
import pysc.models
from examples.util import setup_sensorcloud_basic

MODULE = sys.modules[__name__]
CONSTS = MODULE.CONSTS = dict()

# Define the Endpoint, Username, and Password for use within this file.
CONSTS['SC_ENDPOINT'] = "https://sensor-cloud.io/api/sensor/v2"
CONSTS['SC_USERNAME'] = "your.user@example.com"
CONSTS['SC_PASSWORD'] = "password"
CONSTS['PYSC_DEBUG'] = True

# Define some constants we will use for this example
CONSTS['ORG_ID'] = "csiro"  # This must be an organisation defined on the SensorCloud endpoint beforehand.
CONSTS['NEW_GROUP'] = "mygroup"  # This is the id of the group that will be created in the organisation.
# Set up logging for this example file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    """
    Entrypoint for this example application
    :return:
    """

    # Setup `pysc` to use BASIC auth, with a username, and password. Also sets the endpoint to use.
    setup_sensorcloud_basic(CONSTS['SC_USERNAME'], CONSTS['SC_PASSWORD'],
                            CONSTS['SC_ENDPOINT'], CONSTS['PYSC_DEBUG'])

    org_id = CONSTS['ORG_ID']
    new_group_id = CONSTS['NEW_GROUP']
    # Ensure the organisation exists on the SensorCloud endpoint.
    try:
        organisation = pysc.models.Organisation.single(org_id)
    except KeyError:
        raise RuntimeWarning("""The organisation named {:s} was not found.\n""".format(org_id))
    # Ensure sanity, check we got the organisation that we asked for.
    assert (org_id == organisation.id)

    new_group = pysc.models.Group(new_group_id)  # This is the equiv of calling `models.Group(None, 'group_id', None)`
    # This creates a new group in memory on the client side, but it is not pushed to SensorCloud yet.
    new_group.name = "My New Group"  # Both the .name and .description properties of a Group are mandatory
    new_group.description = "Example of creating a new Group within my organisation in SensorCloud"
    new_group.organisation_id = org_id
    group = new_group.save()  # This sends (saves) the new group to SensorCloud, and receives a Group object in return

    # Important!
    # If there was already a group with the same id on SensorCloud, the existing one will be overwritten!
    # But that is a good thing, because that is the only way you can change or update an existing model on SensorCloud.

    # and finally, sanity check that the group we got back has the same id as the group we sent.
    assert (new_group_id == group.id)


# script execution entrypoint
if __name__ == "__main__":
    main()
