import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# יצירת תיקייה לשמירת התוצרים (בטוחה להעלאה ל-GitHub)
os.makedirs("figures", exist_ok=True)

# טעינת הדאטה הנקי שיצרתם בשלב הקודם
df = pd.read_csv("data/nhanes_40plus_clean.csv")
df["Sex"] = df["RIAGENDR"].map({1: "Men", 2: "Women"})

# ==========================================
# חלק א': הפקת טבלת סיכום (Table 1) ל-README
# ==========================================
summary_rows = []
for group_name, group_df in [
    ("Total Sample (40+)", df),
    ("Men", df[df["Sex"] == "Men"]),
    ("Women", df[df["Sex"] == "Women"]),
]:
  summary_rows.append({
      "Group": group_name,
      "N": len(group_df),
      "Age (Mean ± SD)": (
          f"{group_df['RIDAGEYR'].mean():.1f} ± {group_df['RIDAGEYR'].std():.1f}"
      ),
      "BMI (Mean ± SD)": (
          f"{group_df['BMXBMI'].mean():.1f} ± {group_df['BMXBMI'].std():.1f}"
      ),
      "HGS/BMI (Mean ± SD)": (
          f"{group_df['HGS_BMI'].mean():.2f} ± {group_df['HGS_BMI'].std():.2f}"
      ),
      "Low HGS/BMI (%)": (
          f"{group_df['low_hgs_bmi'].mean()*100:.1f}%"
          f" ({group_df['low_hgs_bmi'].sum()})"
      ),
      "Statins (%)": f"{group_df['is_statin'].mean()*100:.1f}%",
      "Antihypertensives (%)": (
          f"{group_df['is_antihypertensive'].mean()*100:.1f}%"
      ),
      "Antidiabetics (%)": f"{group_df['is_antidiabetic'].mean()*100:.1f}%",
      "Corticosteroids (%)": f"{group_df['is_corticosteroid'].mean()*100:.1f}%",
  })

table1 = pd.DataFrame(summary_rows)
print("--- העתיקו את הטבלה הזו ישירות ל-README.md ---")
print(table1.to_markdown(index=False))

# ==========================================
# חלק ב': הפקת גרף ראשוני (התפלגות HGS/BMI וערכי הסף)
# ==========================================
plt.figure(figsize=(10, 5))
sns.set_style("whitegrid")

# גרף 1: התפלגות HGS/BMI לפי מין עם קווי הסף של FNIH
plt.subplot(1, 2, 1)
sns.boxplot(
    data=df,
    x="Sex",
    y="HGS_BMI",
    palette={"Men": "#4C72B0", "Women": "#DD8452"},
    width=0.4,
)
plt.axhline(
    1.00,
    color="#4C72B0",
    linestyle="--",
    linewidth=1.5,
    label="Men Cutoff (1.00)",
)
plt.axhline(
    0.56,
    color="#DD8452",
    linestyle="--",
    linewidth=1.5,
    label="Women Cutoff (0.56)",
)
plt.title("HGS/BMI Distribution by Sex\n(with FNIH Cutoffs)", fontsize=12)
plt.ylabel("Relative Handgrip Strength (HGS / BMI)")
plt.xlabel("")
plt.legend()

# גרף 2: שכיחות Low HGS/BMI לפי מספר תרופות כרוניות במקביל
plt.subplot(1, 2, 2)
med_cols = [
    "is_statin",
    "is_corticosteroid",
    "is_antihypertensive",
    "is_antidiabetic",
]
df["target_med_count"] = df[med_cols].sum(axis=1)
df["med_group"] = df["target_med_count"].apply(
    lambda x: f"{int(x)}" if x < 3 else "3+"
)

prev_by_meds = (
    df.groupby("med_group")["low_hgs_bmi"].mean().reset_index().sort_values("med_group")
)
sns.barplot(
    data=prev_by_meds, x="med_group", y="low_hgs_bmi", color="#55A868", width=0.5
)
plt.title("Low HGS/BMI Prevalence by\nNumber of Target Medications", fontsize=12)
plt.ylabel("Proportion with Low HGS/BMI")
plt.xlabel("Number of Chronic Med Classes Taken")
plt.ylim(0, max(prev_by_meds["low_hgs_bmi"]) * 1.25)

# הוספת אחוזים מעל העמודות
for index, row in prev_by_meds.iterrows():
  plt.text(
      index,
      row["low_hgs_bmi"] + 0.01,
      f"{row['low_hgs_bmi']*100:.1f}%",
      ha="center",
      fontsize=10,
  )

plt.tight_layout()
plt.savefig("figures/initial_eda_summary.png", dpi=300)
print("\nהגרף נשמר בהצלחה בנתיב: figures/initial_eda_summary.png")
