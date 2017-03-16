#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example of using `pysc` to login to a SensorCloud instance endpoint and delete an existing group from
within your organisation

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
CONSTS['GROUP_ID'] = "mygroup"  # This is the id of the group that will be deleted from the organisation
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
    group_id = CONSTS['GROUP_ID']
    # Ensure the organisation exists on the SensorCloud endpoint.
    try:
        organisation = pysc.models.Organisation.single(org_id)
    except KeyError:
        raise RuntimeWarning("""The organisation named {:s} was not found.""".format(org_id))
    # Ensure sanity, check we got the organisation that we asked for.
    assert (org_id == organisation.id)

    # Ensure the group exists on the SensorCloud endpoint.
    try:
        group = pysc.models.Group.single(group_id)
    except KeyError:
        raise RuntimeWarning("""The group named {:s} was not found.""".format(group_id))
    # Ensure sanity, check we got the group that we asked for.
    assert (group_id == group.id)

    # NOTE! We cannot delete a group that is assigned to any users or groups or anything.
    try:
        pysc.models.Group.delete(group_id, False)  # the second argument is `cascade`, we don't want to do that here.
    except KeyError:
        raise RuntimeError("The group {:s} was not found on the SensorCloud endpoint!".format(group_id))
    group = None
    try:
        group = pysc.models.Group.single(group_id)
    except KeyError:
        # We intend to hit this exception
        print("""The group named {:s} was deleted!.""".format(group_id))
    # Final sanity check, ensure we didn't get an object returned from the Group.single() call above.
    assert group is None


# script execution entrypoint
if __name__ == "__main__":
    main()

