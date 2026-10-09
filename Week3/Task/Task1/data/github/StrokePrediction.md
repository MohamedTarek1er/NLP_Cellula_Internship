# 🫀 Stroke Prediction Project

This project focuses on **predicting whether an individual is at risk of stroke** based on various health and lifestyle factors. The goal is to build a reliable machine learning model that can help identify high-risk patients and potentially aid in early intervention.

---

## 🔍 Project Overview

Stroke is a serious medical condition, and early detection can save lives. In this project, we used a dataset containing demographic, medical, and lifestyle information to predict the likelihood of a stroke. The project includes a full machine learning workflow, from data preprocessing to model evaluation and deployment.

---

## 🛠️ Data Preprocessing

To ensure high-quality inputs for modeling, the following preprocessing steps were applied:  

- **Handling missing values:** Cleaned and imputed missing data.  
- **Encoding categorical variables:** Converted non-numeric features into numeric format.  
- **Feature scaling:** Standardized numerical features for consistent model performance.  
- **Balancing the dataset:** Applied techniques to address class imbalance, ensuring the model does not favor the majority class.  

---

## 📊 Exploratory Data Analysis (EDA)

The EDA phase helped uncover patterns, trends, and relationships in the dataset:  

- Visualizations of feature distributions  
- Analysis of correlations between risk factors and stroke occurrence  
- Insights into how different demographic and lifestyle features affect stroke risk  

---

## 🧩 Feature Engineering

- Created new features and transformed existing ones to enhance model performance  
- Selected the most relevant features to reduce noise and improve accuracy  

---

## 🤖 Machine Learning Models

Several machine learning models were trained and compared to identify the best-performing approach:  

- Logistic Regression  
- Random Forest Classifier  
- XGBoost  
- Support Vector Machine (SVM)  
- K-Nearest Neighbors (KNN)  

Each model was evaluated using standard metrics and fine-tuned for optimal performance.

---

## 📈 Model Evaluation

Models were evaluated using:  

- **ROC Curve:** To assess the trade-off between sensitivity and specificity  
- **Confusion Matrix:** To evaluate true positives, true negatives, false positives, and false negatives  
- **Accuracy, Precision, Recall, and F1-Score:** To quantify overall model performance  

The best model was selected based on its overall performance across these metrics.

---

## ⚡ Conclusion

This project demonstrates a full **end-to-end machine learning workflow** for predicting stroke risk, including preprocessing, exploratory analysis, feature engineering, modeling, and evaluation. It highlights the importance of careful data preparation, feature selection, and model evaluation in building robust predictive solutions.
