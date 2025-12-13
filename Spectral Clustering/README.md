# Spectral Clustering on Non-Linear Datasets

This project investigates **Spectral Clustering** as an alternative to classical clustering algorithms when dealing with **non-linearly separable datasets**.  
The analysis is grounded in **linear algebra concepts**, such as eigenvalues and eigenvectors of graph Laplacians, and compares spectral clustering with standard methods like **K-Means** and **DBSCAN**.

The project focuses on understanding how the construction of similarity graphs and the choice of hyperparameters affect clustering performance.

---

## Project Overview

Two synthetic datasets were analyzed:

- **Circles dataset**: points arranged in concentric circles with an additional globular cluster  
- **Spirals dataset**: three intertwined spiral-shaped clusters

These datasets are well-known examples where traditional clustering algorithms (e.g. K-Means) struggle due to non-globular cluster shapes.

The goal is to:
- build similarity graphs from the data
- compute graph Laplacians
- project data into a lower-dimensional **spectral space**
- apply clustering algorithms in both the original and spectral spaces
- evaluate and compare the results using internal and external metrics

---

## Methodology

### Graph Construction
- computation of the **similarity matrix** using a Gaussian kernel
- construction of **k-nearest-neighbors adjacency matrices**
- conversion to sparse matrix formats (CSR)
- enforcement of symmetry in adjacency matrices

### Spectral Analysis
- computation of the **degree matrix** and **graph Laplacian**
- eigenvalue and eigenvector analysis of the Laplacian
- selection of the number of eigenvectors based on:
  - connected components
  - spectrum structure

### Clustering
Clustering was performed on:
- the **original feature space**
- the **spectral embedding**

Algorithms used:
- **K-Means**
- **DBSCAN**

### Evaluation
Clustering performance was evaluated using:
- **Silhouette Score**
- **Adjusted Rand Index (ARI)**

A systematic comparison was conducted for different values of the neighborhood parameter \( k \) and different embedding dimensions.

---

## Results

- Spectral clustering significantly improves clustering quality on non-linear datasets
- The choice of \( k \) in the similarity graph is critical for performance
- For the Spirals dataset, spectral clustering combined with K-Means achieves a much closer approximation to the ground-truth labels compared to clustering in the original space
- DBSCAN performs well in some cases but is highly sensitive to hyperparameter selection

---

## Notes on Collaboration

This project was developed as a **pair project** in an academic setting.

**My personal contribution focused on:**
- implementation of the spectral clustering pipeline
- construction of similarity, adjacency, degree, and Laplacian matrices
- eigenvalue and eigenvector analysis of the graph Laplacian
- experimentation with different values of neighborhood size and embedding dimensions
- application and comparison of K-Means and DBSCAN in spectral and original spaces
- quantitative evaluation using clustering metrics
- analysis and interpretation of the results

---

## Libraries Used

- Python  
- NumPy  
- SciPy (sparse matrices, linear algebra)  
- scikit-learn  
- Matplotlib  

---

## How to Run

1. Open the notebook or scripts associated with the project.
2. Run the analysis sequentially to reproduce the experiments and figures.
