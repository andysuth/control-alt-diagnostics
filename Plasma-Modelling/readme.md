# Plasma Modelling – Particle-in-Cell Simulations for PWFA

This repository contains simulation input files, scripts, and analysis tools for modelling plasma-based particle acceleration using the Particle-in-Cell (PIC) method. These models are developed for use with [VSim](https://www.txcorp.com/vsim) by Tech-X Corporation.

## 🔬 What is a Particle-in-Cell (PIC) Code?

PIC codes are a class of computational physics tools used to simulate plasma dynamics. They combine:
- **Lagrangian particles** (representing electrons, ions, etc.)
- **Eulerian electromagnetic fields** (solved on a spatial grid)

The particles are moved through the fields, while the fields are updated based on the particle currents and charge densities. This self-consistent loop allows accurate, time-resolved modelling of kinetic effects in plasma.

PIC codes are critical in plasma physics where analytical solutions are impossible, especially in highly non-linear and relativistic regimes.

## 🚀 Relevance to Plasma Wakefield Acceleration (PWFA)

Plasma Wakefield Acceleration is a technique where a high-energy particle beam (the **driver**) excites a strong wake in a plasma, which can accelerate a trailing beam (the **witness**) to very high energies over short distances.

PIC simulations allow researchers to:
- Resolve the femtosecond dynamics of beam-plasma interaction
- Optimise parameters like plasma density, beam profile, and injection timing
- Predict experimental observables with high fidelity

---

## 📁 Repository Contents

- `wideMAL.pre`  
  A VSim preprocessor file defining a 2D3V (2 spatial, 3 velocity components) simulation of a high-energy beam propagating through plasma. It includes:
  
  - **Grid and Time Settings**: Resolution and timestep control for stability and accuracy.
  - **Species Definitions**: Relativistic beam particles, background plasma electrons and ions.
  - **Initial Conditions**: Beam shape, position, and momentum; plasma profiles.
  - **Diagnostics**: Field output, particle tracking, and phase space projections.
  - **Boundary Conditions**: Absorbing or reflecting boundaries as required.
  - **Field Solvers**: Definitions for electromagnetic field updates and Poisson solvers.
 
- `indiSpec.py`
A Python-based post-processing script for analyzing electron energy spectra from VSim PIC simulations. The script:

  - Loads HDF5 particle data dumps for specified species (e.g., electrons from hydrogen and helium)
  - Computes total charge and kinetic energy across simulation time
  - Generates histograms of energy distributions for different spatial regions
  - Calculates **impact ionization yield rates** based on gas-specific cross sections
  - Produces time-resolved plots of:
    - Total charge and energy evolution
    - Instantaneous and cumulative yield
    - Energy spectra with spatial filtering
  - Fits linear trends to cumulative yield vs. time, estimating yield rates in pC/ps

  The script outputs `.png` visualizations and a summary `.txt` file containing quantitative results. It is designed to support kinetic analysis of beam–plasma interactions, especially in the context of plasma wakefield acceleration where secondary ionization plays a role in plasma response and diagnostics.
  
- `initialExample.sl`
A template slurm file for requesting and scheduling the computational resource request

- `TemporalIonizationDesigner`
This MATLAB script generates a 3D spatial distribution of ionization probability ("torch") produced by a laser pulse interacting with a neutral gas target. It uses ADK tunnel ionization theory to compute the instantaneous ionization rate integrated over the laser pulse duration and spatial profile.

The script allows configuring gas species, laser pulse parameters (energy, spot size, duration), and simulation grid resolution to produce a realistic initial plasma distribution. This output can be exported as a formatted particle macro-distribution file for input into PIC codes such as VVSim.

The generated "torch" models the initial ionized plasma shape induced by the laser, which is essential for plasma wakefield acceleration and other laser-plasma interaction studies.

Optional features include visualizing the ionization probability in 2D slices and calculating total ionized charge in specified regions.


---

## 🧰 Requirements

- [VSim](https://www.txcorp.com/vsim) (developed by Tech-X Corporation)  
  VSim is a commercial simulation framework for electromagnetics and plasma physics, with support for PIC simulations.

- HPC or multi-core environment (recommended for performance)

---

## 📜 License

This repository is released under the **GNU General Public License v3.0**.  
You are free to use, modify, and distribute the contents under the same license terms.  
See the [`LICENSE`](LICENSE) file for details.

---

## 🙏 Contributions & Acknowledgments

- Developed as part of research into beam-driven plasma acceleration.
- The `wideMAL.pre` configuration builds on conventions from VSim tutorials and documentation.
- Acknowledgments to Tech-X for their development of VSim and associated documentation.
- Acknowledgments to Paul Scherkl, Thomas Heinemann, and Fahim Habib.

Contributions via pull requests are welcome. For questions, please open an issue or contact the repository owner.

