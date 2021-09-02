# gecoshc-client AppImage

Help Channel client for GECOS workstations.

This Help Channel client validates the workstation against the GECOS CC and then connects to the appropiate Help Channel Server (basically a UVNC Repeater) by using x11vnc.

## Relathionship with other projects

This project includes:

* [websocket-client 0.58.0](https://pypi.python.org/pypi/websocket-client/)

This project is part of the GECOS environment.

## Requirements

Install the package 'appimage-builder' following the [official documentation](https://appimage-builder.readthedocs.io/en/latest/intro/install.html)

## Building

To build this project in a Debian system execute:

``
appimage-builder
``

## Installing

To execute this project use the AppImage:  

``
./helpchannel-1.2.1-x86_64.AppImage
``
