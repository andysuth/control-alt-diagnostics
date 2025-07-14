# Interactive Gaussian Beam Ray Tracer in MATLAB

This project is an interactive ray tracing tool for modeling Gaussian beam propagation through multiple thin lenses using the ABCD matrix formalism. It features a graphical user interface (GUI) for intuitive editing and visualization of optical systems.
##  Features

-  Real-time plotting of beam radius along the propagation axis
-  Dynamic lens table with support for:
  - Position, focal length, aperture width, and material
  - Adding and removing lenses on the fly
- ABCD matrix-based propagation using complex beam parameter formalism
- Visual representation of lenses and beam envelope

##  Technical Overview

The GUI supports interactive modification of lens parameters via a `uitable`, with automatic plot updates. Users can add or remove lenses using GUI buttons and adjust the total propagation length.

## 📷 Interface Snapshot

<img width="1284" height="652" alt="Example" src="https://github.com/user-attachments/assets/699749b2-88b1-4d7f-acbc-308254c4223c" />

## Getting Started

0. MATLAB (R2021a+) required

1. Open `RayTracer_v0.m` in MATLAB and run the script.

2. Use the GUI to:
    - Add/remove lenses
    - Edit lens properties
    - Adjust system length
    - Observe real-time changes in beam propagation

## Author

Created by **Andrew Sutherland**
This project was developed with the assistance of OpenAI’s ChatGPT for code review, and refining GUI behavior in MATLAB.

## TO DO
- Update lens refraction calculation to include refractive index calculation via sellmeier equation to allow different materials.
- Include 'thickness' for modelling non-focusing elements, e.g. viewports and their effect on focusing/waist positioning
- Include estimate for glass bending under vacuum pressure to estimate additional focusing terms

