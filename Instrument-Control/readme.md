### Motorised Optics Control Interfaces

This directory contains Python-based GUIs for controlling two motorised optical components: an iris and a waveplate. The interfaces are built using PyQt5 and are designed for laboratory use with serial or USB-controlled actuators.

## Contents

irisScript.pyPython GUI to control a motorised iris using the XIMC controller. Includes automatic limit finding, percentage-based positioning, and position readout.

irisInterface.uiQt Designer file defining the GUI layout for the iris control application.

waveplateScript.pyPython GUI for controlling a motorised waveplate via a serial COM port. Supports angle-based and transmission-based input, with feedback on current position and calculated transmission.

waveplateInterface.uiQt Designer file defining the GUI layout for the waveplate control application.

## Requirements

Python 3.x

PyQt5

libximc (for iris control)

pyserial (for waveplate control)

## Usage

Run either script from a Cygwin or native Windows Python environment:

python irisScript.py

or

python waveplateScript.py

Make sure the associated .ui files are present in the same directory.



