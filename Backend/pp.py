import pandas as pd
import re
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet',quiet=True)
# =========================
# 🔹 RUN ONLY ONCE (THEN COMMENT)
# =========================
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')

tqdm.pandas()

# =========================
# 🔹 GLOBAL OBJECTS
# =========================
base_stopwords = set(stopwords.words('english'))
custom_stopwords = base_stopwords - {
    'no', 'not', 'with', 'without', 'during', 'before', 'after'
}

lemmatizer = WordNetLemmatizer()
spell = SpellChecker()

important_short_words = {'bp', 'hr', 'iv', 'cp'}
fillers = {'uh', 'hmm', 'idk', 'actually', 'like'}

# Regex
regex_special = re.compile(r'[^a-z\s]')
regex_space = re.compile(r'\s+')
regex_zero = re.compile(r'(?<=\w)0')
regex_one = re.compile(r'(?<=\w)1')

# =========================
# 🔥 BATCH CLEANING (TRAINING)
# =========================
def text_clean_batch(text):
    text = str(text).lower()

    text = " ".join([w for w in text.split() if w not in fillers])

    text = regex_zero.sub('o', text)
    text = regex_one.sub('i', text)

    text = regex_special.sub(' ', text)
    text = regex_space.sub(' ', text).strip()

    tokens = text.split()
    clean_tokens = []

    for word in tokens:

        if word in important_short_words:
            clean_tokens.append(word)
            continue

        if word in custom_stopwords or len(word) <= 2:
            continue

        if len(word) > 5 and word not in spell:
            word = spell.correction(word) or word

        word = lemmatizer.lemmatize(word)
        clean_tokens.append(word)

    return " ".join(clean_tokens)

# =========================
# ⚡ FAST CLEANING (PREDICTION)
# =========================
def text_clean_fast(text):
    text = str(text).lower()

    text = " ".join([w for w in text.split() if w not in fillers])

    text = regex_zero.sub('o', text)
    text = regex_one.sub('i', text)

    text = regex_special.sub(' ', text)
    text = regex_space.sub(' ', text).strip()

    tokens = text.split()

    clean_tokens = [
        lemmatizer.lemmatize(w)
        for w in tokens
        if w not in custom_stopwords and len(w) > 2
    ]

    return " ".join(clean_tokens)

# =========================
# 🔥 REMOVE DISEASE NAMES (LABEL LEAKAGE FIX)
# =========================
def build_disease_remover(df, label_col):
    disease_labels = set(df[label_col].astype(str).str.lower().unique())
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, disease_labels)) + r')\b')
    
    def remove(text):
        return pattern.sub("disease", str(text).lower())
    
    return remove

# =========================
# 🚀 APPLY FUNCTION (MAIN)
# =========================
def preprocess_dataset(df, text_col, label_col, save_path=None):
    """
    Full preprocessing pipeline:
    - Remove disease names
    - Clean text
    - Add clean_text column
    - Optionally save
    """

    print("🚀 Starting preprocessing...")

    # Step 1: Remove disease names
    print("🧠 Removing disease names (label leakage fix)...")
    remove_fn = build_disease_remover(df, label_col)
    df[text_col] = df[text_col].astype(str).progress_apply(remove_fn)

    # Step 2: Clean text
    print("🧹 Cleaning text...")
    df["clean_text"] = df[text_col].progress_apply(text_clean_batch)

    # Step 3: Save (optional)
    if save_path:
        df.to_csv(save_path, index=False)
        print(f"💾 Saved to: {save_path}")

    print("✅ Preprocessing completed!")

    return df

print("done backend/pp.py")
