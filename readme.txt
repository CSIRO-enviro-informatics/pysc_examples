This repository contains worked examples of use cases for the pysc Python SensorCloud library.

These examples assume you have created an account on a SensorCloud instance, and you know the SensorCloud
endpoint that you wish to communicate with.

You must also know the organisation id of the organisation entity that your account was created with.

Some of the examples require just read permission on your account, however some require write permission.

Every example has a CONSTS dict near the top of the file, where you can define things like the url of the
SensorCloud endpoint, your username, and your password. You will need to change these before the examples will work.
Most examples need you to also enter your organisation id in the CONSTS dict for the example to work.

Additional explanation and instructions for each example are included at the top of each file, and in comments
throughout the source code.

The pysc library requires at least Python 3.4, however Python 3.5 is recommended as is what we developed the pysc
library and these examples using. Python 3.6 should work, however it has not been tested.

The pysc library needs to be installed as a discoverable module in your local python installation.
We recommend using pip to install pysc, as it can install the package directly from the Bitbucket repository.
Run the following command to install pysc:
pip3 install -e git+https://bitbucket.csiro.au/scm/eis/pysc.git@master#egg=pysc

Or, using the requirements.txt file:
pip3 install -r requirements.txt

If the pysc library is updated and you wish to use the newer version, upgrade with the following command:
pip3 install --upgrade -e git+https://bitbucket.csiro.au/scm/eis/pysc.git@master#egg=pysc
