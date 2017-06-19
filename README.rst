===============================
Local Builder for delivery.yaml
===============================

Hack to test build_steps of a ``delivery.yaml`` locally with Docker.

Building the base image:

.. code-block::

    docker build -t ubuntu-buildbox .

Usage:

.. code-block::

    cd myproject
    /path/to/build.py delivery.yaml
