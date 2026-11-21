# DataScienceinHealthcare
import pandas as pd

# קריאת קובץ ה-XPT מתוך תיקיית data
df = pd.read_sas("data/MGX_G.XPT", format="xport")

# הצגת 5 השורות הראשונות של הטבלה
print(df.head())

# הצגת גודל הטבלה (כמה שורות וכמה עמודות יש בה)
print("גודל הטבלה:", df.shape)

# Research Plan & Literature Review
**Course:** Data Science in Healthcare (Fall 2026)  
**Domain:** Physiotherapy & Pharmacology — Chronic Medications and Muscle Function  

---

## 1. Research Question
Does integrating cumulative duration of chronic medication use in days (`RXDDAYS`)—specifically statins, corticosteroids, and antihypertensive drugs—into an XGBoost model improve the prediction of reduced relative handgrip strength (`HGS/BMI`) among adults aged 40 and older in the NHANES (2011–2014) dataset, compared to a baseline model relying solely on demographic and anthropometric features?

---

## 2. Dataset: NHANES (2011–2014 Cycles)
* **Source:** CDC National Health and Nutrition Examination Survey (Open Access, SAS `.xpt` format).
* **Target Population:** Adults aged $\ge 40$ years (comparing middle-aged adults 40–64 vs. older adults 65+).
* **Key Modules & Variables:**
  * **Demographics (`DEMO`):** Participant ID (`SEQN`), age, sex, ethnicity.
  * **Muscle Strength (`MGX`):** Maximal handgrip strength (kg), normalized by Body Mass Index (`HGS/BMI`) as the primary outcome.
  * **Body Measures (`BMX`):** Weight, height, BMI, waist circumference.
  * **Prescription Medications (`RXQ_RX`):** Medication names/classes (statins, corticosteroids, antihypertensives) and duration of use in days (`RXDDAYS`).
  * **Lifestyle & Nutrition (`PAQ`, `DR1TOT`):** Physical activity levels and dietary intake (protein, vitamin D, total energy) as covariates.
* **Data Access Note:** Raw `.xpt` files are stored locally under `data/` and excluded from version control via `.gitignore`.

---

## 3. Literature Review

### Paper 1: Same Dataset & Feasibility (NHANES)
* **Citation:** *Handgrip Strength and Muscle Quality: Results from the National Health and Nutrition Examination Survey Database* (*Journal of Clinical Medicine*, 2023).
* **What they did:** Analyzed 14,741 participants from NHANES (2011–2014) combining dynamometer handgrip strength, body composition (BMI and muscle mass), physical activity, and nutritional intake using multiple linear regression.
* **What they found:** Demonstrated non-linear changes in handgrip strength across the lifespan (peaking around ages 18–20 and declining sharply after ages 66–72), with significant positive correlations to muscle mass, BMI, and dietary energy intake.
* **Research Gap (What was left open):**
  1. **Omission of Medication Profiles:** Did not incorporate prescription medication data (`RXQ_RX`) or cumulative exposure duration (`RXDDAYS`), despite known drug-induced myopathy and muscle-weakening mechanisms.
  2. **Linear Modeling Only:** Relied on traditional regression rather than non-linear machine learning (e.g., XGBoost) capable of capturing complex interactions between age, chronic drugs, and nutrition.

### Paper 2: Same Research Question & Modeling Approach (ML for Grip Strength)
* **Citation:** *Machine Learning-Based Model for Grip Strength Prediction in Healthy Adults: A Nationwide Dataset-Based Study* (*Journal of Clinical Medicine*, 2025).
* **What they did:** Used a nationwide health and nutrition survey (KNHANES, $N = 21,147$ adults) to train and compare machine learning models—including XGBoost, Multilayer Perceptron (MLP), and polynomial regression—to predict handgrip strength from anthropometric and physical activity variables.
* **What they found:** XGBoost achieved the highest predictive accuracy and generalization ($R^2 = 0.717$), outperforming both neural networks and classical regression, with weight, age, height, and waist circumference serving as top predictors.
* **Research Gap (What was left open):**
  1. **Healthy Cohort Bias:** The study excluded individuals with chronic conditions and did not include chronic medication use or exposure duration.
  2. **Absolute vs. Relative Strength:** Predicted absolute grip strength rather than body-size-normalized relative handgrip strength (`HGS/BMI`), which is a stronger clinical indicator of functional decline and frailty.

---

## 4. Planned Methodology & Novelty
1. **Clinical Synergy:** Combines functional physiotherapy metrics (`HGS/BMI`) with pharmacological exposure metrics (`RXDDAYS`).
2. **Baseline vs. Full Model:** Compare a demographic/anthropometric XGBoost baseline against a full XGBoost model incorporating medication classes, exposure duration, and nutritional/activity covariates.
3. **Explainability:** Apply **SHAP** values to evaluate the relative importance of medication duration compared to physical activity and nutrition across age subgroups (40–64 vs. 65+).
