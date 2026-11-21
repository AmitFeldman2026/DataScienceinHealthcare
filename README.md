#טבלת הסיכום

| Group | N | Age (Mean ± SD) | BMI (Mean ± SD) | HGS/BMI (Mean ± SD) | Low HGS/BMI (%) | Statins (%) | Antihypertensives (%) | Antidiabetics (%) | Corticosteroids (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Sample (40+)** | 6,421 | 59.1 ± 12.0 | 29.3 ± 6.9 | 1.24 ± 0.45 | 7.2% (462) | 27.8% | 44.8% | 16.4% | 2.2% |
| **Men** | 3,129 | 59.2 ± 12.0 | 28.7 ± 5.8 | 1.54 ± 0.39 | 8.0% (251) | 29.6% | 43.6% | 17.3% | 1.9% |
| **Women** | 3,292 | 59.0 ± 12.1 | 30.0 ± 7.6 | 0.96 ± 0.29 | 6.4% (211) | 26.0% | 46.0% | 15.6% | 2.5% |

![Initial EDA Summary](figures/initial_eda_summary.png)

**ממצאים ראשוניים (EDA):**
מדגם המחקר הסופי שלנו כולל **6,421 נבדקים בני 40 ומעלה** מתוך מחזורי NHANES 2011–2014, כאשר **7.2% מהם (462 נבדקים)** עומדים בהגדרה הקלינית של FNIH לכוח אחיזת יד יחסי נמוך (`HGS/BMI < 1.00` לגברים ו-`< 0.56` לנשים). כפי שניתן לראות בגרף, שכיחות חולשת השרירים עולה בחדות ככל שמספר קבוצות התרופות הכרוניות הנלקחות במקביל גדל — מ-**2.8%** בקרב נבדקים שאינם נוטלים אף אחת מהתרופות הללו, ל-**6.5%** (תרופה אחת), **13.3%** (2 תרופות), ועד **18.8%** בקרב מי שנוטלים 3 קבוצות תרופות או יותר. מגמת עלייה חדה זו מחזקת את הצורך לבדוק האם אינטראקציות לא-ליניאריות בין סוגי תרופות ספציפיים (באמצעות מודל XGBoost) משפרות את יכולת הניבוי מעבר לספירת תרופות פשוטה ולמודלים ליניאריים.

**Initial Exploratory Findings:**
Our final analytical cohort includes **6,421 adults aged 40+** from the NHANES 2011–2014 cycles, with an overall prevalence of **7.2% (462 cases)** meeting the FNIH clinical criteria for low relative handgrip strength (`HGS/BMI < 1.00` for men and `< 0.56` for women). As shown in the figure above, the prevalence of low `HGS/BMI` increases sharply with concurrent use of our target chronic medication classes—rising from **2.8%** among individuals taking none of these medications to **6.5%** (1 class), **13.3%** (2 classes), and **18.8%** (3+ classes). This steep upward trend provides strong preliminary motivation to investigate whether non-linear interactions between specific drug classes (modeled via XGBoost) improve risk prediction beyond simple medication counts and linear models.


