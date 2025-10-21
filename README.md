# Airline Price Analysis — Data Analytics Project

## Overview
The objective of the study is to analyse the flight booking dataset obtained from “Ease My Trip” website and to conduct various statistical hypothesis tests in order to get meaningful information from it. 'Easemytrip' is an internet platform for booking flight tickets, and hence a platform that potential passengers use to buy tickets. A thorough study of the data will aid in the discovery of valuable insights that will be of enormous value to passengers.

---

## Repository Structure

│── notebooks/  
│   ├── data_cleaning_v1.ipynb — Initial Data cleaning file
│   ├── xx.ipynb — 
│   ├── xx.ipynb — 
 
│── data/  
│   ├── raw_data/ — Original dataset  
│   ├── clean_data/ — Clean dataset 

  
│── figures/
│── SQL/


│── config.yaml — File paths configuration  
│── README.md — Project documentation  

---

## Data Inputs
- **Dataset source:** [Flight Price Prediction] (https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction)
- **Main features:**  
  `xx`, `xx`, `xx`,
- **Target variable:** `xx`
- **Data version:** `xx`

All paths are configured in `config.yaml`.

---

## Feature Engineering
- Extracted car brand from the `name` column.  
- Applied One-Hot Encoding to `fuel`, `seller_type`, and `transmission`.  
- Applied Ordinal Encoding to `owner`.  
- Created new feature `car_age = 2025 - year`.  
- Scaled numerical features with **MinMaxScaler** and normalized with **PowerTransformer**.  
- Checked **feature correlations** to avoid redundancy.  
- Removed extreme outliers in the `selling_price` column after transformation.

---

## Models and Evaluation

### Baseline Models
- **K-Nearest Neighbors (KNN)**  
- **Linear Regression**

### Ensemble and Advanced Models
- **Bagging Regressor (Decision Tree base)**  
- **Pasting Regressor (Decision Tree base)**  
- **Random Forest Regressor**  
- **Gradient Boosting Regressor**  
- **AdaBoost Regressor**

Each model was evaluated using:
- **MAE** (Mean Absolute Error)  
- **MSE** (Mean Squared Error)  
- **RMSE** (Root Mean Squared Error)  
- **R²** (Coefficient of Determination)

**Best performing model:**  
 `Random Forest Regressor` — **R² ≈ 0.93**

---

## Useful Links  

- [Kanban Board (Trello)] - 


- [Google Slides Presentation] - 


---
