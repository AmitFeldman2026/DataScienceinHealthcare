# Literature Review & Research Question

## Research Question
Does integrating chronic medication profiles (specifically drug classes such as statins and corticosteroids, along with duration of use in days) and nutritional intake into an XGBoost model improve the prediction of reduced relative handgrip strength (HGS/BMI) in adults aged 40 and older in the NHANES dataset, compared to models based solely on demographic and anthropometric features?

---

## Selected Dataset
* **Dataset:** National Health and Nutrition Examination Survey (NHANES), 2011–2012 and 2013–2014 cycles.
* **Key Modules:** 
  * Demographics (`DEMO`)
  * Muscle Strength – Grip (`MGX`)
  * Prescription Medications (`RXQ_RX`, including duration variable `RXDDAYS`)
  * Body Measures (`BMX`) & Dietary Intake (`DR1TOT`)
* **Access:** Publicly available open-access SAS transport files (`.xpt`) via the CDC website.

---

## Literature Review (Two Core Papers)

### Paper 1: Same Dataset & Feasibility
* **Title:** Handgrip Strength and Muscle Quality: Results from the National Health and Nutrition Examination Survey Database
* **Journal & Year:** *Journal of Clinical Medicine*, 2023
* **Link:** [PubMed Central (PMC10179381)](https://nih.gov)
* **What they did:** Analyzed cross-sectional data from 14,741 participants in the NHANES 2011–2014 cycles, combining digital dynamometer handgrip strength measurements with body composition (BMI, muscle mass), physical activity, and dietary intake using multivariable linear regression models.
* **What they found:** Handgrip strength exhibits a non-linear trajectory across the lifespan (peaking around ages 18–20 and declining sharply after ages 66–72) and correlates positively with muscle mass, BMI, and total energy intake.
* **What is left open (Our Gap):** The study did not incorporate prescription medication data or duration of drug exposure (`RXDDAYS`), and relied on traditional linear regression rather than non-linear machine learning models capable of capturing complex drug–nutrition interactions.

### Paper 2: Same Research Question & Methodology
* **Title:** Machine Learning-Based Model for Grip Strength Prediction in Healthy Adults: A Nationwide Dataset-Based Study
* **Journal & Year:** *Journal of Clinical Medicine*, 2025
* **Link:** [MDPI Full Text](https://mdpi.com)
* **What they did:** Trained and compared multiple machine learning models—including XGBoost, Multilayer Perceptron (MLP), and polynomial regression—on 21,147 adults from a national health and nutrition survey (KNHANES) to predict handgrip strength from anthropometric and physical activity variables.
* **What they found:** XGBoost achieved the highest predictive accuracy and generalization performance ($R^2 = 0.717$), outperforming both neural networks and classical regression, with weight, age, height, and waist circumference serving as the top predictors.
* **What is left open (Our Gap):** The model was restricted to healthy adults and excluded chronic medication profiles, cumulative exposure duration, and detailed dietary micronutrients.

---

## Our Novel Contribution
Our project bridges the gap between these two studies by applying the top-performing non-linear algorithm (**XGBoost** with SHAP explainability) from Paper 2 to the multi-modal **NHANES 2011–2014** dataset validated in Paper 1. Specifically, we introduce three novel dimensions:
1. **Medication Exposure Duration:** Utilizing `RXDDAYS` to distinguish between short-term use and long-term chronic exposure (e.g., >1 year on statins or corticosteroids).
2. **Relative Handgrip Strength:** Normalizing maximum grip strength by BMI (`HGS / BMI`) to account for body size confounding.
3. **Middle-Aged Stratification:** Expanding the analysis beyond older adults (65+) to include middle-aged adults (40–64) for earlier detection of medication-associated muscle decline.
