# Bank Marketing Data Analysis  

This project analyzes a **Bank Marketing dataset**, which contains customer demographic and campaign-related information.  
The main goal is to explore and preprocess the data in order to understand the factors that influence whether a customer subscribes to a term deposit (`y`).  

## 🎯 Target Column  
- **y**: Indicates whether the customer subscribed to a term deposit.  
  - `1` → Subscribed  
  - `0` → Not Subscribed  

## 🧾 Dataset Features  

### 👤 Customer Information  
- **age**: Age of the customer (numerical)  
- **marital**: Marital status (married, single, divorced)  
- **education**: Education level (secondary, tertiary, unknown)  
- **job**: Job type (management, technical, blue-collar, services, student, retired, housewife, unemployed)  
- **housing**: Housing status (own, rent)  
- **loan**: Whether the customer had a previous loan (yes/no)  

### 📞 Campaign & Contact Details  
- **contact**: Contact communication type (telephone, cellular)  
- **day**: Day of the week of the last contact (numerical)  
- **month**: Month of last contact (numerical)  
- **duration**: Duration of last contact in seconds (numerical)  
- **campaign**: Number of contacts during the campaign (numerical)  
- **previous**: Number of previous contacts before this campaign (numerical)  
- **pdays**: Days passed since the customer was last contacted in a previous campaign (numerical)  

---

## 🔑 Project Workflow  

### 🧹 Data Cleaning & Preprocessing  
- Handling missing values and unknown categories  
- Encoding categorical variables (job, education, marital, housing, loan, etc.)  
- Feature scaling for numerical attributes (age, duration, campaign, pdays)  
- Outlier detection in duration and campaign-related features  

### 📊 Exploratory Data Analysis (EDA)  
- Survival rate analysis: proportion of customers subscribing vs. not subscribing  
- Visualizations with **Matplotlib** and **Seaborn**:  
  - Subscription distribution by marital status, education, and job  
  - Age distribution and its impact on subscription  
  - Contact duration vs. subscription likelihood  
- Interactive charts with **Plotly** for deeper exploration  

### 🛠️ Tools & Libraries Used  
- **Pandas, NumPy** → data manipulation and preprocessing  
- **Matplotlib, Seaborn, Plotly** → visualization and dashboards  
- **Scikit-learn (preprocessing)** → encoding and scaling utilities  
- **Jupyter Notebook** → step-by-step analysis and documentation  

---

📌 This project demonstrates how **data analysis techniques** can be applied to a marketing dataset to understand customer behavior and the factors influencing the success of subscription campaigns.  
