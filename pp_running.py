import pandas as pd
from pp import preprocess_dataset

# =========================
# LOAD RAW DATASET
# =========================
df = pd.read_csv(r"E:\OneDrive\Documents\Healix AI\DATA\final_symptoms_to_disease (1).csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

print("Columns:", df.columns)

# =========================
# SET YOUR COLUMNS
# =========================
TEXT_COL = "symptom_text"
LABEL_COL = "diseases"

# =========================
# APPLY PREPROCESSING
# =========================
df = preprocess_dataset(
    df,
    text_col=TEXT_COL,
    label_col=LABEL_COL,
    save_path=r"E:\OneDrive\Documents\Healix AI\DATA\cleaned_dataset.csv"
)

print("\n✅ Dataset cleaned and saved!")