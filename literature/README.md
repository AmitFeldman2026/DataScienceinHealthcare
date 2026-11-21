import pandas as pd

# קריאת קובץ ה-XPT מתוך תיקיית data
df = pd.read_sas("data/MGX_G.XPT", format="xport")

# הצגת 5 השורות הראשונות של הטבלה
print(df.head())

# הצגת גודל הטבלה (כמה שורות וכמה עמודות יש בה)
print("גודל הטבלה:", df.shape)
