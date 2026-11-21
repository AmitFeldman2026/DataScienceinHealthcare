import pandas as pd
import numpy as np

# ==========================================
# 1. טעינת מילון התרופות וזיהוי 4 הקבוצות
# ==========================================
drug_dict = pd.read_sas("data/RXQ_DRUG.XPT", encoding='latin1')

cat_cols = [c for c in drug_dict.columns if c.startswith('RXDDCN')]
drug_dict['all_categories'] = drug_dict[cat_cols].fillna('').agg(' | '.join, axis=1).str.lower()

drug_dict['is_statin'] = drug_dict['all_categories'].str.contains('statins').astype(int)
drug_dict['is_corticosteroid'] = drug_dict['all_categories'].str.contains('glucocorticoids|adrenal cortical steroids').astype(int)
drug_dict['is_antihypertensive'] = drug_dict['all_categories'].str.contains(
    'antihypertensive|ace inhibitors|angiotensin|beta-adrenergic|calcium channel|diuretics'
).astype(int)
drug_dict['is_antidiabetic'] = drug_dict['all_categories'].str.contains('antidiabetic|insulin').astype(int)

drug_map = drug_dict[['RXDDRGID', 'is_statin', 'is_corticosteroid', 'is_antihypertensive', 'is_antidiabetic']].drop_duplicates()

# ==========================================
# 2. פונקציה לטעינה ואיחוד של מחזור דו-שנתי
# ==========================================
def process_cycle(suffix):
    demo = pd.read_sas(f"data/DEMO_{suffix}.XPT")
    bmx = pd.read_sas(f"data/BMX_{suffix}.XPT")
    mgx = pd.read_sas(f"data/MGX_{suffix}.XPT")
    rx = pd.read_sas(f"data/RXQ_RX_{suffix}.XPT", encoding='latin1')
    
    # תיקון: חישוב הכוח המקסימלי שנמדד ביד אחת מתוך כל 6 הניסיונות (3 בימין, 3 בשמאל)
    trial_cols = ['MGXH1T1', 'MGXH1T2', 'MGXH1T3', 'MGXH2T1', 'MGXH2T2', 'MGXH2T3']
    mgx['MAX_HGS_ONE_HAND'] = mgx[trial_cols].max(axis=1)
    
    # הצלבת תרופות הנבדק עם המילון
    rx_merged = rx.merge(drug_map, on='RXDDRGID', how='left')
    med_cols = ['is_statin', 'is_corticosteroid', 'is_antihypertensive', 'is_antidiabetic']
    rx_merged[med_cols] = rx_merged[med_cols].fillna(0)
    rx_merged['total_meds'] = rx_merged['RXDCOUNT'].fillna(0)
    
    rx_patient = rx_merged.groupby('SEQN', as_index=False).agg({
        'is_statin': 'max',
        'is_corticosteroid': 'max',
        'is_antihypertensive': 'max',
        'is_antidiabetic': 'max',
        'total_meds': 'max'
    })
    
    # איחוד הטבלאות לפי SEQN (עם העמודה החדשה MAX_HGS_ONE_HAND)
    df = demo[['SEQN', 'RIDAGEYR', 'RIAGENDR', 'RIDRETH3']].merge(
        bmx[['SEQN', 'BMXBMI']], on='SEQN', how='inner'
    ).merge(
        mgx[['SEQN', 'MAX_HGS_ONE_HAND']], on='SEQN', how='inner'
    ).merge(
        rx_patient, on='SEQN', how='inner'
    )
    
    df['cycle'] = suffix
    return df

# ==========================================
# 3. איחוד שני המחזורים וסינון אוכלוסיית המחקר
# ==========================================
df_g = process_cycle("G") # 2011-2012
df_h = process_cycle("H") # 2013-2014
df_full = pd.concat([df_g, df_h], ignore_index=True)

df_clean = df_full[
    (df_full['RIDAGEYR'] >= 40) &
    (df_full['BMXBMI'].notna()) &
    (df_full['MAX_HGS_ONE_HAND'].notna())
].copy()

# ==========================================
# 4. הגדרת משתנה המטרה (Low HGS/BMI) לפי ספי FNIH
# ==========================================
# כעת מחלקים ישירות את מקסימום היד החזקה ב-BMI (ללא חלוקה ב-2)
df_clean['HGS_BMI'] = df_clean['MAX_HGS_ONE_HAND'] / df_clean['BMXBMI']

df_clean['low_hgs_bmi'] = np.where(
    ((df_clean['RIAGENDR'] == 1) & (df_clean['HGS_BMI'] < 1.00)) |
    ((df_clean['RIAGENDR'] == 2) & (df_clean['HGS_BMI'] < 0.56)),
    1, 0
)

df_clean.to_csv("data/nhanes_40plus_clean.csv", index=False)

print(f"Total clean sample size (age 40+): {len(df_clean)}")
print(f"Low HGS/BMI prevalence: {df_clean['low_hgs_bmi'].mean():.1%} ({df_clean['low_hgs_bmi'].sum()} cases)")
print("\nMedication counts in sample:")
print(df_clean[['is_statin', 'is_corticosteroid', 'is_antihypertensive', 'is_antidiabetic']].sum())
