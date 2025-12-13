# PCA-Based People Profile Analysis

This project explores the use of **Principal Component Analysis (PCA)** for the analysis and representation of people profiles based on high-dimensional data.  
The goal is to reduce dimensionality while preserving the most informative components of the original data, enabling clearer interpretation, visualization, and downstream analysis.

The project is implemented in a **Jupyter Notebook** and focuses on understanding how PCA can be applied in practice to real-world datasets involving human-related features.

---

## Project Overview

High-dimensional datasets often contain redundant or highly correlated features, making analysis and visualization difficult.  
This project applies **PCA** to:
- compress the original feature space
- identify dominant patterns in the data
- analyze how much variance is captured by each principal component
- represent individuals using a lower-dimensional embedding

---

## Methodology

The workflow implemented in the notebook includes:

### 1. Data Preparation
- loading and inspection of the dataset
- normalization / standardization of features
- handling of numerical representations suitable for PCA

### 2. Principal Component Analysis
- computation of the covariance matrix
- eigenvalue and eigenvector analysis
- projection of the data onto principal components
- evaluation of explained variance

### 3. Dimensionality Reduction
- selection of the optimal number of components
- comparison between original and reduced representations
- analysis of information loss versus dimensionality reduction

### 4. Interpretation and Visualization
- visualization of data in the reduced PCA space
- interpretation of principal components
- analysis of similarities and differences between individual profiles

---

## Results

The application of PCA demonstrates that:
- a limited number of principal components can capture a large portion of the total variance
- dimensionality reduction enables clearer visualization and interpretation of people profiles
- PCA is an effective tool for feature compression and exploratory data analysis

---

## Technologies Used

- Python  
- NumPy  
- Pandas  
- Matplotlib / Seaborn  
- Jupyter Notebook  

---

## Notes

This project was developed as a pair project in an academic activity focused on **linear algebra and data analysis techniques**.  
The notebook reflects my direct involvement in the core analytical pipeline and in the interpretation of PCA as a dimensionality reduction technique.

---

## How to Run

1. Open the notebook:
   ```bash
   jupyter notebook PCA_people_profiles.ipynb
