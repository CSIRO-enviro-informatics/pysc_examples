#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example of using `pysc` to login to a SensorCloud instance endpoint and retrieve a selection of observations from
a given stream.

Note, the `pysc` lib, (and by extension these examples) require python 3.4 or above. Preferably use python 3.5 for best
compatibility and performance. 3.6 _should_ work, but it is not tested.
"""
__author__ = "Ashley Sommer"
__copyright__ = "Copyright 2017, CSIRO Land and Water"

import logging
import sys
import pysc.models
from datetime import datetime, timedelta
from examples.util import setup_sensorcloud_basic, datetime_from_iso

MODULE = sys.modules[__name__]
CONSTS = MODULE.CONSTS = dict()

# Define the Endpoint, Username, and Password for use within this file.
CONSTS['SC_ENDPOINT'] = "https://sensor-cloud.io/api/sensor/v2"
CONSTS['SC_USERNAME'] = "your.user@example.com"
CONSTS['SC_PASSWORD'] = "password"
CONSTS['PYSC_DEBUG'] = True

# Define some constants we will use for this example
CONSTS['STREAM_ID'] = "my.stream.1"  # The stream from which we want to get observations

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
    try:
        stream = pysc.models.Stream.single(stream_id)
    except KeyError:
        raise RuntimeWarning("""The stream named {:s} was not found.\n""".format(stream_id))
    # Ensure sanity, check we got the stream that we asked for.
    assert (stream_id == stream.id)

    # get observations in chunks of 1000 results at a time
    chunk_size = 1000
    offset = datetime.min

    while True:
        obs = stream.filtered_observations(limit=chunk_size, start=offset)
        c = len(obs.results)
        if c < 1:
            break
        results = obs.results
        last_time = offset
        for r in results:
            time = r['t']
            time = datetime_from_iso(time)
            if time > last_time:
                last_time = time
            val = r['v']
            if isinstance(val, dict):
                val = val['v']
            print("Found observation result: {:s}: {:f}".format(str(time), val))
        # add one second to the offset to avoid overlap with the final result in the last set
        offset = last_time + timedelta(seconds=1)

# script execution entrypoint
if __name__ == "__main__":
    main()
