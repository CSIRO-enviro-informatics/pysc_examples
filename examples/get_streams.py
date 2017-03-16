#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example of using `pysc` to login to a SensorCloud instance endpoint and retrieve all of the visible Streams
belonging to a given organisation.

Note, the `pysc` lib, (and by extension these examples) require python 3.4 or above. Preferably use python 3.5 for best
compatibility and performance. 3.6 _should_ work, but it is not tested.
"""
__author__ = "Ashley Sommer"
__copyright__ = "Copyright 2017, CSIRO Land and Water"

import logging
import sys
import pysc.models
from haleasy import LinkNotFoundError
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

    # use the organisation_id param to filter streams based on id
    stream_index = pysc.models.Stream.index(params={'organisation_id': org_id})
    stream_count = 0
    while True:
        stream_links = stream_index.links(rel="streams")
        # using the `.links()` helper on the index, we get a list of HALLink objects, not stream objects.
        # we have to do `.follow()` on each one to turn it into a HAL object.
        # Note, even after we do .follow() on the link, it is still not a `pysc` Stream() object, but a raw HAL object.
        # See the get_groups.py example for an example of using `.resolve_all()` rather than `.index()`
        for s in stream_links:
            stream_count += 1
            stream = s.follow()
            stream_id = stream['id']  # We have to use ['id'] because it is a raw HAL object, not a Stream() object.
            print("Found stream: {:s}".format(stream_id))
        try:
            next_index = stream_index.link(rel="next")
            stream_index = next_index.follow()
        except LinkNotFoundError:
            break
    print("Found a total of {:d} streams for {:s} on that SensorCloud endpoint.".format(stream_count, org_id))

# script execution entrypoint
if __name__ == "__main__":
    main()
