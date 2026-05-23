import pandas as pd
import joblib
import time

from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

start_time = time.time()

print("🚀 Loading dataset...")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(
    r"E:\OneDrive\Documents\Healix AI\DATA\cleaned_dataset.csv"
)

# Remove very small texts
df = df[
    df["clean_text"].str.split().str.len() > 2
]

print(f"✅ Dataset Loaded: {len(df)} rows")

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    df["clean_text"],
    df["diseases"],
    test_size=0.2,
    stratify=df["diseases"],
    random_state=42
)

print("✅ Train-Test Split Completed")

# =========================
# LABEL ENCODING
# =========================
le = LabelEncoder()

y_train_enc = le.fit_transform(y_train)
y_test_enc  = le.transform(y_test)

print(f"✅ Total Disease Classes: {len(le.classes_)}")

# =========================
# MODEL
# =========================
base_model = LinearSVC(
    class_weight='balanced'
)

# =========================
# CALIBRATED MODEL
# =========================
calibrated_model = CalibratedClassifierCV(
    estimator=base_model,
    method='sigmoid',
    cv=3
)

# =========================
# PIPELINE
# =========================
pipeline = Pipeline([

    ("tfidf", TfidfVectorizer(
        max_features=10000,
        ngram_range=(1,3),
        min_df=2,
        max_df=0.95
    )),

    ("clf", calibrated_model)

])

print("🤖 Training model with probability calibration...")

# =========================
# TRAIN
# =========================
pipeline.fit(
    X_train,
    y_train_enc
)

print("✅ Training Completed")

# =========================
# EVALUATION
# =========================
print("\n📊 Evaluating model...")

y_pred = pipeline.predict(X_test)

print("\n📊 Model Performance:\n")

print(
    classification_report(
        y_test_enc,
        y_pred
    )
)

# =========================
# PROBABILITY TEST
# =========================
print("\n🧪 Testing probability output...")

sample_text = ["high fever headache body pain"]

sample_probs = pipeline.predict_proba(sample_text)[0]

top_idx = sample_probs.argmax()

top_disease = le.inverse_transform([top_idx])[0]

top_confidence = round(
    float(sample_probs[top_idx] * 100),
    2
)

print(f"\n✅ Sample Prediction: {top_disease}")
print(f"✅ Confidence: {top_confidence}%")

# =========================
# SAVE MODEL
# =========================
SAVE_PATH = r"C:\Healix AI\Notebooks\disease_model.joblib"

joblib.dump({

    "pipeline": pipeline,

    "label_encoder": le

}, SAVE_PATH)

print(f"\n💾 Model saved successfully!")
print(f"📁 Path: {SAVE_PATH}")

# =========================
# TIME TRACKING
# =========================
end_time = time.time()

total_time = round(
    end_time - start_time,
    2
)

print(f"\n⏱️ Total Time: {total_time} sec")
print("\n🚀 Healix AI Training Completed Successfully!")