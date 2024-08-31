.. _to10.0_deps_install:

=============================
Dependencies and installation
=============================

In most cases, your existing PyTango devices and clients will continue to
work as before, however there are important changes. In the other sections of
the migration guide, you can find the incompatibilities and the necessary migration steps.

Dependencies
============

PyTango v10.0.0 requires Python 3.9 or higher.

PyTango v10.0.0 moved from `cppTango`_ 9.5.x to at least 10.0.0.  It
will not run with earlier versions.

PyTango is compiled with Numpy 2.x , but can work with both 1.x and 2.x versions at runtime.

PyTango 10.0.0 has a many new *optional* dependencies, related to the support of OpenTelemetry:

    #. "opentelemetry-api"
    #. "opentelemetry-sdk"
    #. "opentelemetry-exporter-otlp-proto-grpc"
    #. "opentelemetry-exporter-otlp-proto-http"

The easiest way to install all of them when using pip is:

.. sourcecode:: console

    pip install "pytango[telemetry]"

For conda packages, the dependencies are automatically included on Linux and macOS, and
excluded on Windows.

Depending on the installed packages you may have the following options:

#. Telemetry support not compiled into cppTango:

    * No telemetry (but dummy functions available for same API)

#. Telemetry support compiled into cppTango:

    * Python OpenTelemetry API and SDK dependencies installed:  full functionality
    * Python OpenTelemetry API dependency installed, but not SDK dependency:  partial functionality - functions calls propagate telemetry information, but no traces are emitted (the tracing backend will show missing traces)
    * Python OpenTelemetry dependencies not installed: no telemetry, but dummy functions available for same API

Please refer to the MR description for instructions on getting started with OpenTelemetry: https://gitlab.com/tango-controls/pytango/-/merge_requests/708

Installation
============

Similar to the 9.4.x and 9.5.x series, the binary wheels on `PyPI`_ and `Conda-forge`_ make installation very simple on many
platforms.  No need for compilation.  See :ref:`Getting started <getting-started>`.
