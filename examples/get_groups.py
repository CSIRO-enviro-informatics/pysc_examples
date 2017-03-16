#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example of using `pysc` to login to a SensorCloud instance endpoint and retrieve all of the known Groups
within to a given organisation.

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

    # Ensure the organisation exists on the SensorCloud endpoint.
    try:
        organisation = pysc.models.Organisation.single(org_id)
    except KeyError:
        raise RuntimeWarning("""The organisation named {:s} was not found.\n"""
                             """Although the `pysc` api has functionality to create an organisation, it cannot """
                             """do so on the sensor-cloud.io instance on AWS.""".format(org_id))
    # Ensure sanity, check we got the organisation that we asked for.
    assert (org_id == organisation.id)

    # Here we use the Group.resolve_all helper with organisation_id param to filter groups based on id
    # The resolve_all command is similar to .index() however it also calls .follow() on found link automatically,
    # _and_ it converts the resulting HAL objects into real valid `pysc` Group() objects.
    org_groups = pysc.models.Group.resolve_all(params={'organisation_id': org_id})
    # We are not likely to have more than 1000 groups, so we don't need to do return doc pagination here.
    for g in org_groups:
        group_id = g.id
        print("Found group: {:s}".format(group_id))

    print("Found a total of {:d} groups for {:s} on that SensorCloud endpoint.".format(len(org_groups), org_id))

# script execution entrypoint
if __name__ == "__main__":
    main()
