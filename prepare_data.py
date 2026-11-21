import pandas as pd
import numpy as np

# ==========================================
# 1. טעינת מילון התרופות וזיהוי 4 הקבוצות
# ==========================================
drug_dict = pd.read_sas("data/RXQ_DRUG.XPT", encoding='latin1')

# איחוד כל עמודות הסיווג הפרמקולוגי (רמות 1, 2 ו-3) לטקסט אחד לכל תרופה
cat_cols = [c for c in drug_dict.columns if c.startswith('RXDDCN')]
drug_dict['all_categories'] = drug_dict[cat_cols].fillna('').agg(' | '.join, axis=1).str.lower()

# הגדרת מילות מפתח רשמיות של מילון Multum לכל אחת מ-4 קבוצות התרופות
# 1. סטטינים: statins (תת-קטגוריה של antihyperlipidemic agents)
drug_dict['is_statin'] = drug_dict['all_categories'].str.contains('statins').astype(int)

# 2. קורטיקוסטרואידים: glucocorticoids / adrenal cortical steroids (ללא משחות/טיפות עיניים מקומיות אם רוצים סיסטמי, או כלל הסטרואידים)
drug_dict['is_corticosteroid'] = drug_dict['all_categories'].str.contains('glucocorticoids|adrenal cortical steroids').astype(int)

# 3. תרופות ללחץ דם: antihypertensive / beta-adrenergic / ace inhibitors / angiotensin / calcium channel / diuretics
drug_dict['is_antihypertensive'] = drug_dict['all_categories'].str.contains(
    'antihypertensive|ace inhibitors|angiotensin|beta-adrenergic|calcium channel|diuretics'
).astype(int)

# 4. תרופות לסוכרת: antidiabetic agents / insulin / sulfonylureas / biguanides
drug_dict['is_antidiabetic'] = drug_dict['all_categories'].str.contains('antidiabetic|insulin').astype(int)

# שמירת טבלת המיפוי הנקייה: קוד תרופה -> 4 דגלים בינאריים
drug_map = drug_dict[['RXDDRGID', 'is_statin', 'is_corticosteroid', 'is_antihypertensive', 'is_antidiabetic']].drop_duplicates()

# ==========================================
# 2. פונקציה לטעינה ואיחוד של מחזור דו-שנתי
# ==========================================
def process_cycle(suffix):
    demo = pd.read_sas(f"data/DEMO_{suffix}.XPT")
    bmx = pd.read_sas(f"data/BMX_{suffix}.XPT")
    mgx = pd.read_sas(f"data/MGX_{suffix}.XPT")
    rx = pd.read_sas(f"data/RXQ_RX_{suffix}.XPT", encoding='latin1')
    
    # הצלבת תרופות הנבדק עם המילון שייצרנו
    rx_merged = rx.merge(drug_map, on='RXDDRGID', how='left')
    
    # מילוי 0 למי שלא לוקח תרופות (RXDUSE == 2) או לתרופות שלא שייכות ל-4 הקבוצות
    med_cols = ['is_statin', 'is_corticosteroid', 'is_antihypertensive', 'is_antidiabetic']
    rx_merged[med_cols] = rx_merged[med_cols].fillna(0)
    
    # מספר התרופות הכולל שהנבדק לוקח (RXDCOUNT חסר כאשר RXDUSE == 2, לכן ממלאים 0)
    rx_merged['total_meds'] = rx_merged['RXDCOUNT'].fillna(0)
    
    # קיבוץ לשורה אחת לכל נבדק (SEQN): לוקחים מקסימום (1 אם לוקח לפחות תרופה אחת מהקבוצה)
    rx_patient = rx_merged.groupby('SEQN', as_index=False).agg({
        'is_statin': 'max',
        'is_corticosteroid': 'max',
        'is_antihypertensive': 'max',
        'is_antidiabetic': 'max',
        'total_meds': 'max'
    })
    
    # איחוד כל הטבלאות של המחזור לפי SEQN
    df = demo[['SEQN', 'RIDAGEYR', 'RIAGENDR', 'RIDRETH3']].merge(
        bmx[['SEQN', 'BMXBMI']], on='SEQN', how='inner'
    ).merge(
        mgx[['SEQN', 'MGDCGSZ']], on='SEQN', how='inner'
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

# סינון: גיל 40 ומעלה, ללא ערכים חסרים ב-BMI, בכוח אחיזת יד או בתרופות
df_clean = df_full[
    (df_full['RIDAGEYR'] >= 40) &
    (df_full['BMXBMI'].notna()) &
    (df_full['MGDCGSZ'].notna())
].copy()

# ==========================================
# 4. הגדרת משתנה המטרה (Low HGS/BMI) לפי ספי FNIH
# ==========================================
# חישוב היחס: כוח אחיזת יד מקסימלי (ק"ג) חלקי BMI
df_clean['HGS_BMI'] = df_clean['MGDCGSZ'] / df_clean['BMXBMI']

# ערכי הסף הקליניים של FNIH (Studenski et al., 2014):
# גברים (RIAGENDR == 1): מתחת ל-1.00
# נשים (RIAGENDR == 2): מתחת ל-0.56
df_clean['low_hgs_bmi'] = np.where(
    ((df_clean['RIAGENDR'] == 1) & (df_clean['HGS_BMI'] < 1.00)) |
    ((df_clean['RIAGENDR'] == 2) & (df_clean['HGS_BMI'] < 0.56)),
    1, 0
)

# שמירת הדאטה המעובד מקומית (בתוך תיקיית data/ שלא עולה ל-GitHub!)
df_clean.to_csv("data/nhanes_40plus_clean.csv", index=False)

# הדפסת סיכום נתונים להכנסה ישירה ל-README.md
print(f"Total clean sample size (age 40+): {len(df_clean)}")
print(f"Low HGS/BMI prevalence: {df_clean['low_hgs_bmi'].mean():.1%} ({df_clean['low_hgs_bmi'].sum()} cases)")
print("\nMedication counts in sample:")
print(df_clean[['is_statin', 'is_corticosteroid', 'is_antihypertensive', 'is_antidiabetic']].sum())
