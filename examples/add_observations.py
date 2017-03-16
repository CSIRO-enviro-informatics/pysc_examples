#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example of using `pysc` to login to a SensorCloud instance endpoint and add observations to an existing stream.
See the create_stream.py example for creating a stream first!
See get_observations_from_stream.py for an example of reading back these observations you have put up.

Note, the `pysc` lib, (and by extension these examples) require python 3.4 or above. Preferably use python 3.5 for best
compatibility and performance. 3.6 _should_ work, but it is not tested.
"""
__author__ = "Ashley Sommer"
__copyright__ = "Copyright 2017, CSIRO Land and Water"

import logging
import sys
import random
from datetime import datetime, timedelta
import pysc.models
from examples.util import setup_sensorcloud_basic, datetime_to_iso

MODULE = sys.modules[__name__]
CONSTS = MODULE.CONSTS = dict()

# Define the Endpoint, Username, and Password for use within this file.
CONSTS['SC_ENDPOINT'] = "https://sensor-cloud.io/api/sensor/v2"
CONSTS['SC_USERNAME'] = "your.user@example.com"
CONSTS['SC_PASSWORD'] = "password"
CONSTS['PYSC_DEBUG'] = True

# Define some constants we will use for this example
# Note, adding observations to stream is one of the only things for which we don't need to include our organisation_id.
CONSTS['STREAM_ID'] = "my.stream.1"  # This is the id of the stream that will be created in the organisation.
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

    stream_id = CONSTS['STREAM_ID']
    # Ensure the stream exists on the SensorCloud endpoint.
    try:
        stream = pysc.models.Stream.single(stream_id)
    except KeyError:
        raise RuntimeWarning("""The stream named {:s} was not found.""".format(stream_id))
    # Ensure sanity, check we got the stream that we asked for.
    assert (stream.id == stream.id)
    generated_results = []
    obs = pysc.models.Observation(None, stream=stream)  # The None just means we are creating a new observation
    # The following block just generates a chunk of 100 hourly observation results
    starting_time = datetime.now() - timedelta(hours=100)  # an arbitrary starting time
    for i in range(1, 100):
        generated_results.append({"t": datetime_to_iso(starting_time + timedelta(hours=i)),
                                  "v": {"v": random.random() * 10.0}})
    # add our list of results to the observation
    obs.results = generated_results
    obs.save()  # Save here actually uploads the observation results to the stream. We don't get anything back.
    # see the get_observations_from_stream.py example to read these observation results

# script execution entrypoint
if __name__ == "__main__":
    main()
