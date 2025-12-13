# Speaker Age Prediction from Audio

This project focuses on the **prediction of a speaker’s age from spoken audio signals** using Machine Learning techniques.  
The task is formulated as a **regression problem**, where the model estimates the speaker’s age as a continuous variable based on acoustic and linguistic features extracted from `.wav` files.

The project lies at the intersection of **speech processing** and **machine learning**, exploring how vocal characteristics correlate with biological traits such as age.

---

## Project Overview

The dataset is composed of:
- **Development set**: 2,933 audio samples with ground-truth age labels (used for training and validation)
- **Evaluation set**: 691 audio samples without age labels (used for final evaluation)

Each sample is described by a combination of:
- acoustic features (e.g. pitch, jitter, shimmer, spectral centroid)
- temporal features (e.g. silence duration, number of pauses)
- linguistic metadata (e.g. gender, ethnicity)

The objective is to design a robust ML pipeline capable of extracting meaningful information from speech signals and producing accurate age predictions.

---

## Methodology

### Feature Engineering
Significant effort was devoted to **feature engineering**, including:
- preprocessing and encoding of categorical metadata (gender, ethnicity)
- extraction of acoustic features from audio signals
- computation of **MFCCs (Mel-Frequency Cepstral Coefficients)** from spectrograms
- window-based MFCC statistics (mean, standard deviation, max)
- introduction of additional handcrafted features such as **words per second**

Feature importance analysis was used to guide feature selection and refinement.

---

### Machine Learning Pipeline
A complete end-to-end pipeline was implemented, including:
- data preprocessing and cleaning
- train/validation splitting
- model evaluation with multiple regressors
- selection of **Random Forest Regressor** as the most suitable model
- development of **gender-specific models** to better capture vocal differences

---

### Training and Hyperparameter Tuning
- model training was performed using scikit-learn
- **Grid Search** was applied for hyperparameter tuning (number of estimators, max depth)
- evaluation metrics included **RMSE**, **MAE**, and **R² score**

The final solution achieved competitive performance on the evaluation set.

---

### Testing and Evaluation
- systematic testing across different feature configurations
- comparison with baseline models
- analysis of dataset imbalance and its impact on predictions
- discussion of limitations and possible future improvements

---

## Results
The final model achieved:
- **RMSE ≈ 9.8**
- improved performance compared to baseline regressors
- stable generalization on unseen data

---

## Notes on Collaboration

This project was developed as a **pair project** in an academic setting.

**My personal contribution focused on:**
- feature engineering and feature selection  
- design and implementation of the ML pipeline  
- model training and validation  
- hyperparameter tuning  
- testing, evaluation, and result analysis  

---

## Technologies Used
- Python
- NumPy, Pandas
- scikit-learn
- Audio processing libraries
- Machine Learning regression models
