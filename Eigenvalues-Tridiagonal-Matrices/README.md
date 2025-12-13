# Eigenvalues of Tridiagonal Symmetric Matrices

This project studies the **eigenvalue computation of symmetric tridiagonal matrices**, combining **theoretical linear algebra tools** with **numerical methods**.  
In particular, Gershgorin’s Circle Theorem is used to bound the spectrum of the matrix, while a Newton-based approach is applied to accurately compute individual eigenvalues.

---

## Project Overview

The analysis focuses on a class of **symmetric, tridiagonal, and diagonally dominant matrices**, which guarantees:
- real eigenvalues
- positive definiteness
- non-singularity

By exploiting these structural properties, it is possible to:
- bound the location of eigenvalues using **Gershgorin’s circles**
- isolate subintervals containing single eigenvalues
- efficiently compute eigenvalues via **Newton’s method**

---

## Methodology

### Spectral Bounds
- application of **Gershgorin’s Circle Theorem** to identify a tight interval containing all eigenvalues
- proof of positivity and non-singularity of the matrix
- refinement of eigenvalue localization using properties of irreducible matrices

### Interval Isolation
- construction of truncated characteristic polynomials
- use of sign variation counting to determine how many eigenvalues lie in a given interval
- iterative interval refinement to isolate a single eigenvalue

### Numerical Computation
- application of **Newton’s method** to the characteristic polynomial
- careful selection of the initial guess based on spectral bounds
- fast convergence due to accurate initialization

---

## Results

The proposed approach allows:
- accurate computation of all eigenvalues
- fast convergence (few iterations per eigenvalue)
- validation of theoretical spectral bounds through numerical results

The method proves to be efficient for structured matrices, while highlighting its limitations when matrix assumptions are violated.

---

## Notes on Collaboration

This project was developed as a **pair project** in an academic setting.

**My contribution focused on** the theoretical analysis of eigenvalue bounds using Gershgorin’s theorem, the design of the interval-isolation strategy, and the numerical implementation and analysis of the Newton-based eigenvalue computation.

---



