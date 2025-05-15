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

