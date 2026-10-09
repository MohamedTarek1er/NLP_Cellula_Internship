# Heart Disease Prediction Using Machine Learning

## Project Overview
This project focuses on building a comprehensive machine learning pipeline to predict heart disease risk based on demographic, lifestyle, and clinical features. The goal is to support early risk identification by leveraging data-driven insights and advanced predictive models, while maintaining strong interpretability suitable for medical-related applications.

The project follows a complete end-to-end workflow, starting from data exploration and analysis, through preprocessing and feature engineering, to model training, evaluation, and deployment.

---

## Dataset Description
The dataset contains medical, lifestyle, and behavioral attributes such as age, gender, blood pressure, cholesterol levels, diabetes status, smoking habits, stress level, sleep hours, and family history of heart disease.  
The target variable represents the **presence or absence of heart disease**.

---

## Exploratory Data Analysis (EDA)
A detailed exploratory analysis was conducted to understand the structure and quality of the data and to extract meaningful insights.

### Key EDA Steps:
- Identified potential data issues such as missing values, outliers, and inconsistencies.
- Analyzed numerical features using histograms, box plots, violin plots, and density-based visualizations.
- Analyzed categorical features using count plots and proportion-based plots.
- Studied relationships between features and the target variable using:
  - Individual feature analysis
  - Feature vs target analysis
  - Integrated visualizations involving two or more features (e.g., lifestyle factors, demographics, and medical indicators).
- Extracted and documented insights after each visualization to highlight patterns, trends, and potential risk factors influencing heart disease.

---

## Data Preprocessing
The preprocessing stage ensured data quality and model readiness:
- Handled missing values using appropriate strategies.
- Verified the absence of significant outliers and duplicate records.
- Ensured consistent data types and valid feature ranges.

---

## Feature Engineering
To enhance model performance and capture higher-level patterns, multiple new features were engineered, including aggregated lifestyle and risk-related indicators.  
In total, **six new engineered features** were added to enrich the dataset and better represent real-world cardiovascular risk factors.

---

## Data Preparation
- Split the dataset into training and testing sets.
- Encoded categorical variables:
  - **Binary features** using Label Encoding.
  - **Ordinal features** using Ordinal Encoding based on domain knowledge.
- Addressed class imbalance using **SMOTE oversampling**, improving minority class representation.
- Scaled numerical features using **Min-Max Scaling**, which showed the best performance among tested scaling methods.

---

## Feature Relevance Analysis
Feature importance and relevance were evaluated using multiple approaches:
- Correlation analysis tailored to feature types (numerical, categorical, ordinal).
- Mutual Information scores to capture non-linear relationships.
- Model-based evaluation to assess the impact of removing or retaining specific features.

Final feature selection decisions were made based on a combination of statistical relevance and model performance.

---

## Model Training and Selection
Multiple machine learning models were trained and compared, both with and without dimensionality reduction (PCA):

### Models Evaluated:
- Logistic Regression
- Support Vector Machine (SVM)
- XGBoost
- LightGBM
- CatBoost
- Simple Multi-Layer Perceptron (MLP)

Hyperparameter tuning was performed using **Grid Search** to optimize performance.

---

## Model Evaluation
Models were evaluated using comprehensive performance metrics, including:
- F1-score
- Precision and Recall
- Confusion Matrix
- Classification Report

Special attention was given to **recall performance on the minority class**, which is critical in medical prediction tasks.  
Based on balanced performance, robustness, and generalization ability, **CatBoost** was selected as the final model.

---

## Deployment
- Saved the trained model, encoders, and scaler for reuse.
- Developed an interactive **Streamlit web application** to enable real-time heart disease risk prediction.
- The deployed system allows users to input patient information and receive instant predictive feedback.

---

## Conclusion
This project demonstrates a complete machine learning lifecycle applied to a real-world medical prediction problem. By combining thorough exploratory analysis, robust preprocessing, advanced modeling, and practical deployment, the system provides both strong predictive performance and meaningful interpretability.

The approach highlights the importance of data understanding, careful feature engineering, and proper evaluation when working with healthcare-related data.

---

## Technologies Used
- Python
- Pandas, NumPy
- Scikit-learn
- XGBoost, LightGBM, CatBoost
- TensorFlow / Keras
- Plotly, Matplotlib, Seaborn
- Streamlit

---
