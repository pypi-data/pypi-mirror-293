*******************************
Pupil Labs LSL Relay
*******************************

The Pupil Labs LSL Relay (Relay) allows you to stream gaze and event data from your
Pupil Invisible device to the `labstreaminglayer <https://github.com/sccn/labstreaminglayer>`_ (LSL).

* For integration between Neon and LSL, use the `Neon Companion app's built-in LSL support <https://docs.pupil-labs.com/neon/data-collection/lab-streaming-layer/>`_.
* For integration between Pupil Core software and LSL, see https://github.com/labstreaminglayer/App-PupilLabs instead.

Install and Usage
==================
Install the Pupil Labs LSL Relay with pip::

   pip install lsl-relay

After you installed the relay, you can start it by executing::

   lsl_relay

The Relay takes the following optional arguments:

- ``--time_sync_interval`` is used to set the interval (in seconds) at which the relay sends events
  to the Pupil Companion device that can be used for time synchronization. The default is 60 seconds.

- ``--timeout`` is used to define the maximum time (in seconds) the relay will search the network for new
  devices before returning. The default is 10 seconds.

- ``--log_file_name`` defines the name and path of the log file. The default is ``lsl_relay.log``.

- ``--device_address IP:PORT`` connects directly to the specified device. Network device discovery and selection
  are skipped. The correct format to pass the device address is ``device_ip:device_port`` the ip address and
  the port of your device can be found in the companion app under Menu -> Streaming.

- ``--outlet_prefix PREFIX`` sets the prefix of the outlet name displayed in lab recorder. The default prefix
  is ``pupil_labs``. Each outlet will also have a suffix, specifying the data stream type (Gaze or Event)

.. caution::
   The Relay currently relies on `NTP`_ for time synchronization between the phone and
   the computer running the relay application. See the :ref:`timestamp_docs` section for
   details.

.. important::
   Make sure the version of your Pupil Labs Companion App is at least v1.4.14 or higher.
   You can download the latest version of the App in the Play Store on your Pupil Labs Companion device.


.. _NTP: https://en.wikipedia.org/wiki/Network_Time_Protocol

.. toctree::
   :maxdepth: 2
   :glob:

   guides/index.rst
   api.rst
   history.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
