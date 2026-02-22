---
date: 2011-01-23
name: N-D Stokes Solver
thumb: /images/ndsolver/logo.svg
---

[ndsolver](https://github.com/meawoppl/ndsolver) is a Python module for solving n-dimensional Stokes flow in periodic porous media. It grew out of graduate research on permeability estimation — simulating low Reynolds number fluid flow through complex porous geometries to compute effective transport properties.

The solver uses finite-difference methods on staggered grids (cell-centered pressure, face-centered velocities) with periodic boundary conditions. A symbolic equation assembly system generates the finite-difference stencils, and sparse matrix construction keeps memory manageable for large domains.

It supports multiple solver backends — direct sparse solvers, LU factorization for repeated solves, and iterative Krylov methods (BiCGSTAB, GMRES). There's also optional JAX support for GPU-accelerated solving. A "big mode" uses memory-mapped arrays and HDF5 storage for domains too large to fit in RAM.

Domains can be imported from images or generated procedurally. The CLI handles batch processing of HDF5 files with per-direction flow simulation and configurable convergence criteria.
