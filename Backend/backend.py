from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pp import text_clean_fast
import joblib
import numpy as np

# =====================================================
# LOAD MODEL
# =====================================================
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "disease_model2.joblib"
)

saved = joblib.load(MODEL_PATH)

pipeline = saved["pipeline"]
label_encoder = saved["label_encoder"]

print("✅ Model Loaded Successfully")
print("✅ Classifier Type:", type(pipeline.named_steps["clf"]))

# =====================================================
# FASTAPI
# =====================================================

app = FastAPI(
    title="Healix AI Backend",
    version="2.0"
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# REQUEST SCHEMA
# =====================================================

class SymptomRequest(BaseModel):
    text: str

# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {
        "message": "Healix AI Backend Running 🚀",
        "disease_classes": len(label_encoder.classes_)
    }

# =====================================================
# ANALYZE
# =====================================================

@app.post("/analyze")
def analyze(req: SymptomRequest):

    try:

        # =====================================================
        # CLEAN TEXT
        # =====================================================

        cleaned_text = text_clean_fast(req.text)

        # =====================================================
        # PREDICT PROBABILITIES
        # =====================================================

        probs = pipeline.predict_proba(
            [cleaned_text]
        )[0]

        # =====================================================
        # TOP PREDICTION
        # =====================================================

        top_idx = np.argmax(probs)

        disease = label_encoder.inverse_transform(
            [top_idx]
        )[0]

        confidence = round(
            float(probs[top_idx] * 100),
            2
        )

        # =====================================================
        # TOP 3 PREDICTIONS
        # =====================================================

        top3_indices = np.argsort(probs)[-3:][::-1]

        top3 = []

        for idx in top3_indices:

            disease_name = label_encoder.inverse_transform(
                [idx]
            )[0]

            conf = round(
                float(probs[idx] * 100),
                2
            )

            top3.append({

                "disease": disease_name,

                "confidence": conf

            })

        # =====================================================
        # RETURN RESPONSE
        # =====================================================

        return {

            "success": True,

            "input_text": req.text,

            "cleaned_text": cleaned_text,

            "disease": disease,

            "confidence": confidence,

            "top3": top3,

            "disease_count": len(
                label_encoder.classes_
            )
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )