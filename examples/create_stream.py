#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example of using `pysc` to login to a SensorCloud instance endpoint and create a new data stream within your
organisation. Also includes example of creating a Location entity if it doesn't exist.

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
CONSTS['LOCATION_ID'] = "brisbane.esp.site.1"
CONSTS['NEW_STREAM_ID'] = "my.stream.1"  # This is the id of the stream that will be created in the organisation.
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
    location_id = CONSTS['LOCATION_ID']
    stream_id = CONSTS['NEW_STREAM_ID']
    # Ensure the organisation exists on the SensorCloud endpoint.
    try:
        organisation = pysc.models.Organisation.single(org_id)
    except KeyError:
        raise RuntimeWarning("""The organisation named {:s} was not found.\n""".format(org_id))
    # Ensure sanity, check we got the organisation that we asked for.
    assert (org_id == organisation.id)

    # First we must ensure we have our location in the SensorCloud. If not, we will create it.
    try:
        location = pysc.models.Location.single(location_id)
    except KeyError:
        # it doesn't exist, so we will create it. We know the details
        new_location = pysc.models.Location(location_id)
        new_location.organisation_id = org_id
        new_location.geo_json = pysc.models.Location.GeoJSON(lat=-27.494743, lon=153.030034)
        new_location.description = "ESP Site in Brisbane"
        location = new_location.save()  # Upload it to SensorCloud, and then use it for our stream.

    new_stream = pysc.models.Stream(stream_id)  # The equiv of calling `models.Stream(None, 'stream_id', None)`
    # This creates a new stream in memory on the client side, but it is not pushed to SensorCloud yet.
    new_stream.name = "My New Stream"  # Both the .name and .description properties of a Stream are mandatory
    new_stream.description = "Example of creating a new Stream within my organisation in SensorCloud"
    new_stream.organisation_id = org_id
    new_stream.location_id = location.id
    new_stream.result_type = pysc.models.Stream.ResultTypes.scalar.value  # Usually scalar
    new_stream.reporting_period = "PT1H"  # Expected reporting_period period in ISO8601 duration format
    new_stream.sample_period = "PT1H"  # Expected sample period in ISO8601 duration format

    # The rest of the metadata on the stream is stored in Metadata object. Lets create one.
    metadata = pysc.models.Stream.Metadata()
    # cumulative will be True or False. It is usually false unless you know it *is* cumulative.
    metadata.cumulative = False
    # Interpolation type will usually be either continuous, or discontinuous, but there are lots of others.
    metadata.interpolation_type = pysc.models.Stream.Metadata.InterpolationTypes.discontinuous.value
    # A text-version of a timezone. This is required when cumulative is True, optional otherwise.
    metadata.timezone = "Australia/Brisbane"
    # Unit of Measure and Observed Property are always required.
    # These URIs must match the white-listed sources of the SensorCloud instance.
    # Check for their existence on the SensorCloud vocabulary first
    metadata.unit_of_measure = "http://registry.it.csiro.au/def/environment/unit/CubicMetresPerCubicMetre"
    metadata.observed_property = "http://data.sense-t.org.au/registry/def/sop/soil_moisture"

    new_stream.stream_metadata = metadata
    stream = new_stream.save()  # This sends (saves) the new stream to SensorCloud, and receives a Stream object

    # Important!
    # If there was already a stream with the same id on SensorCloud, the existing one will be overwritten!
    # But that is a good thing, because that is the only way you can change or update an existing model on SensorCloud.

    # and finally, sanity check that the stream we got back has the same id as the stream we sent.
    assert (stream_id == stream.id)


# script execution entrypoint
if __name__ == "__main__":
    main()
