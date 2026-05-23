import streamlit as st
import requests
import os
import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Healix AI · Health Insights",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# CONFIG
# =====================================================

BACKEND_URL  = "https://healix-ai-powered-health-insights.onrender.com/analyze"
LINKEDIN_URL = "https://www.linkedin.com/in/aryan-hajaria-466a54318/"
YOUR_NAME    = "Aryan Hajaria"
PHOTO_PATH   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.jpg")

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&display=swap');

#MainMenu, footer, header { visibility: hidden; }
*, *::before, *::after { box-sizing: border-box; }

html, .stApp {
    background: #f0f5ee;
    font-family: 'DM Sans', sans-serif;
}
.block-container {
    max-width: 1160px !important;
    padding: 0 2rem 4rem !important;
    margin: 0 auto !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f0f5ee; }
::-webkit-scrollbar-thumb { background: #a8d5a2; border-radius: 99px; }

/* NAVBAR */
.navbar {
    background: #fff;
    border: 1.5px solid #ddeeda;
    border-radius: 20px;
    padding: 16px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 24px;
    margin-bottom: 36px;
    box-shadow: 0 2px 18px rgba(46,125,50,0.06);
}
.navbar-left { display:flex; align-items:center; gap:14px; }
.navbar-logo {
    width:42px; height:42px;
    background: linear-gradient(135deg,#2e7d32,#66bb6a);
    border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    font-size:21px;
}
.navbar-name {
    font-family:'DM Serif Display',serif;
    font-size:32px; color:#1a3d1e; letter-spacing:-0.5px;
}
.navbar-sub {
    font-size:10px; letter-spacing:2.5px; color:#8aab8e;
    font-weight:600; text-transform:uppercase; margin-top:1px;
}
.nav-right { display:flex; align-items:center; gap:32px; }
.nav-link { color:#4a7050; font-size:14px; font-weight:500; text-decoration:none; }
.nav-link:hover { color:#1b5e20; }
.nav-pill {
    background:#e8f5e9; color:#2e7d32;
    border:1.5px solid #c8e6c9; border-radius:99px;
    padding:8px 18px; font-size:13px; font-weight:700;
}

/* HERO */
.pill {
    display:inline-flex; align-items:center; gap:8px;
    background:#e8f5e9; color:#2e7d32;
    border:1.5px solid #c8e6c9; border-radius:99px;
    padding:9px 18px; font-size:13px; font-weight:700;
    margin-bottom:20px;
}
.hero-title {
    font-family:'DM Serif Display',serif;
    font-size:74px; line-height:1.04;
    color:#1a3d1e; letter-spacing:-2px; margin-bottom:16px;
}
.hero-title .green { color:#2e7d32; }
.hero-sub {
    font-size:16.5px; color:#5a7a5e; line-height:1.8;
    max-width:470px; font-weight:400;
}
.hero-sub strong { color:#2e7d32; font-weight:600; }

/* METRICS */
.metrics {
    display:grid; grid-template-columns:1fr 1fr 1fr;
    gap:13px; margin-top:34px;
}
.mc {
    background:#fff; border:1.5px solid #ddeeda;
    border-radius:18px; padding:22px 20px;
    transition: transform .2s, box-shadow .2s;
}
.mc:hover { transform:translateY(-2px); box-shadow:0 8px 22px rgba(46,125,50,.10); }
.mc-icon { font-size:21px; margin-bottom:9px; }
.mc-lbl {
    font-size:11px; font-weight:700; color:#8aab8e;
    text-transform:uppercase; letter-spacing:1.5px; margin-bottom:5px;
}
.mc-val {
    font-family:'DM Serif Display',serif;
    font-size:34px; color:#1a3d1e; line-height:1;
}
.mc-val.g { color:#2e7d32; }

/* PROFILE CARD */
.pc {
    background:#fff; border:1.5px solid #ddeeda;
    border-radius:24px; padding:34px 26px;
    text-align:center;
    box-shadow:0 2px 18px rgba(46,125,50,.06);
}
.pc-avatar {
    width:108px; height:108px; border-radius:50%;
    background:linear-gradient(135deg,#2e7d32,#66bb6a);
    display:inline-flex; align-items:center; justify-content:center;
    font-size:42px; color:#fff;
    border:4px solid #c8e6c9; margin-bottom:18px;
    position:relative;
}
.pc-dot {
    position:absolute; bottom:4px; right:4px;
    width:22px; height:22px;
    background:#4caf50; border:3px solid #fff; border-radius:50%;
}
.pc-name {
    font-family:'DM Serif Display',serif;
    font-size:26px; color:#1a3d1e;
    margin:0 0 6px; letter-spacing:-.4px;
}
.pc-role { font-size:13px; color:#8aab8e; margin-bottom:22px; }
.pc-role span {
    display:inline-block; background:#f0f5ee;
    padding:3px 10px; border-radius:99px; margin:2px;
}
.li-btn {
    display:block;
    background:linear-gradient(135deg,#2e7d32,#388e3c);
    color:#fff !important; text-decoration:none;
    border-radius:12px; padding:13px 22px;
    font-size:14px; font-weight:700;
    box-shadow:0 4px 14px rgba(46,125,50,.28);
    transition: transform .2s, box-shadow .2s;
}
.li-btn:hover { transform:translateY(-2px); box-shadow:0 8px 22px rgba(46,125,50,.35); }
.pc-tag {
    margin-top:13px; font-size:12px; color:#8aab8e;
    font-weight:600; letter-spacing:.5px;
}

/* DIVIDER */
.divider {
    border:none; height:1.5px;
    background:linear-gradient(to right,transparent,#ddeeda,transparent);
    margin:36px 0;
}

/* ANALYSIS HEADER */
.ah {
    background:#fff; border:1.5px solid #ddeeda;
    border-radius:20px; padding:26px 30px;
    display:flex; align-items:center; gap:18px;
    margin-bottom:14px;
    box-shadow:0 2px 12px rgba(46,125,50,.05);
}
.ah-icon {
    width:50px; height:50px;
    background:linear-gradient(135deg,#e8f5e9,#c8e6c9);
    border-radius:14px;
    display:flex; align-items:center; justify-content:center;
    font-size:24px; flex-shrink:0;
}
.ah-title {
    font-family:'DM Serif Display',serif;
    font-size:28px; color:#1a3d1e; margin:0 0 3px; letter-spacing:-.4px;
}
.ah-desc { font-size:14.5px; color:#7a9a7e; margin:0; }

/* TEXTAREA */
.stTextArea > div > div > textarea {
    border:2px solid #ddeeda !important;
    border-radius:16px !important;
    background:#fff !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:15px !important; color:#2d4a31 !important;
    padding:16px 18px !important; min-height:120px !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextArea > div > div > textarea:focus {
    border-color:#4caf50 !important;
    box-shadow:0 0 0 3px rgba(76,175,80,.12) !important;
    outline:none !important;
}
.stTextArea > label { display:none !important; }

/* BUTTON */
.stButton > button {
    background:linear-gradient(135deg,#2e7d32,#43a047) !important;
    color:#fff !important; border:none !important;
    border-radius:14px !important; font-size:16px !important;
    font-weight:700 !important; width:100% !important;
    height:54px !important;
    box-shadow:0 4px 16px rgba(46,125,50,.28) !important;
    letter-spacing:.3px !important;
    transition: transform .2s, box-shadow .2s !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 24px rgba(46,125,50,.35) !important;
}

/* TIPS */
.tips-lbl {
    font-size:11px; font-weight:700; color:#8aab8e;
    text-transform:uppercase; letter-spacing:1.2px; margin-bottom:8px;
}
.tips-row { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; }
.tip {
    background:#fff; border:1.5px solid #ddeeda;
    border-radius:99px; padding:7px 14px;
    font-size:12.5px; color:#5a7a5e; font-weight:500;
    cursor:pointer; transition:all .15s;
}
.tip:hover { background:#e8f5e9; border-color:#a5d6a7; color:#2e7d32; }

/* RESULTS */
.rp {
    background:linear-gradient(135deg,#1b5e20,#2e7d32);
    border-radius:20px; padding:30px;
    color:#fff; margin-bottom:14px; position:relative; overflow:hidden;
}
.rp::before {
    content:''; position:absolute;
    top:-28px; right:-28px;
    width:150px; height:150px;
    background:rgba(255,255,255,.07); border-radius:50%;
}
.rp-lbl {
    font-size:11px; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; opacity:.65; margin-bottom:8px;
}
.rp-name {
    font-family:'DM Serif Display',serif;
    font-size:40px; letter-spacing:-1px; margin-bottom:14px;
}
.conf-bar {
    background:rgba(255,255,255,.18);
    border-radius:99px; height:9px; margin-bottom:9px; overflow:hidden;
}
.conf-fill {
    height:100%; border-radius:99px;
    background:linear-gradient(90deg,#a5d6a7,#fff);
}
.conf-num { font-size:28px; font-weight:800; opacity:.95; }
.conf-sub { font-size:12px; opacity:.6; margin-top:2px; }

.rs {
    background:#fff; border:1.5px solid #ddeeda;
    border-radius:18px; padding:22px 24px; margin-bottom:13px;
}
.st-lbl {
    font-family:'DM Serif Display',serif;
    font-size:20px; color:#1a3d1e; margin-bottom:3px;
}
.st-sub { font-size:12.5px; color:#8aab8e; margin-bottom:14px; }

.t3g { display:grid; grid-template-columns:1fr 1fr 1fr; gap:11px; margin-top:14px; }
.t3c {
    background:#f0f5ee; border:1.5px solid #ddeeda;
    border-radius:14px; padding:16px; text-align:center;
    transition: transform .2s;
}
.t3c:hover { transform:translateY(-2px); }
.t3-rank {
    font-size:10px; font-weight:700; color:#8aab8e;
    text-transform:uppercase; letter-spacing:1px; margin-bottom:7px;
}
.t3-name {
    font-family:'DM Serif Display',serif;
    font-size:16px; color:#1a3d1e; margin-bottom:5px;
}
.t3-pct { font-size:24px; font-weight:800; color:#2e7d32; }

.cleaned {
    background:#f8faf7; border:1.5px solid #ddeeda;
    border-radius:13px; padding:14px 18px;
    font-family:monospace; font-size:13.5px;
    color:#3a5e40; margin-top:14px; word-break:break-all;
}

/* DISCLAIMER */
.disc {
    background:#fffbee; border:1.5px solid #f0d060;
    border-radius:20px; padding:26px 30px;
    display:flex; gap:18px; align-items:flex-start; margin-top:34px;
}
.disc-icon { font-size:26px; flex-shrink:0; margin-top:2px; }
.disc-title {
    font-family:'DM Serif Display',serif;
    font-size:19px; color:#7a5800; margin-bottom:7px;
}
.disc-body { font-size:14px; color:#8a6a00; line-height:1.8; }
.disc-body strong { color:#7a5000; }

/* FOOTER */
.ft {
    text-align:center; padding:30px 0 6px;
    font-size:12.5px; color:#9ab89e; letter-spacing:.2px;
}
.ft a { color:#5a9a5e; text-decoration:none; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ---- NAVBAR ----
st.markdown("""
<nav class="navbar">
  <div class="navbar-left">
    <div class="navbar-logo">🌿</div>
    <div>
      <div class="navbar-name">Healix AI</div>
      <div class="navbar-sub">AI-Powered Health Insights</div>
    </div>
  </div>
  <div class="nav-right">
    <a class="nav-link" href="#">Analysis</a>
    <a class="nav-link" href="#">About</a>
    <a class="nav-link" href="#">Safety</a>
    <div class="nav-pill">🎓 Educational Model</div>
  </div>
</nav>
""", unsafe_allow_html=True)

# ---- HERO + PROFILE ----
left, right = st.columns([2.1, 1], gap="large")

with left:
    st.markdown(f"""
    <div class="pill">🧠 Clinical NLP Interface</div>
    <div class="hero-title">Healix <span class="green">AI</span></div>
    <div class="hero-sub">
        AI-powered symptom analysis for educational healthcare insights —
        with <strong>SHAP explainability</strong> so you understand every prediction.
    </div>
    <div class="metrics">
      <div class="mc"><div class="mc-icon">🦠</div><div class="mc-lbl">Diseases</div><div class="mc-val">254</div></div>
      <div class="mc"><div class="mc-icon">🧠</div><div class="mc-lbl">NLP Engine</div><div class="mc-val g">Active</div></div>
      <div class="mc"><div class="mc-icon">💡</div><div class="mc-lbl">SHAP XAI</div><div class="mc-val g">On</div></div>
    </div>
    """, unsafe_allow_html=True)

with right:
    from PIL import ImageDraw

    def make_circle_img(path, size=220):
        """Crop to square, resize, apply circular mask → return PIL RGBA image."""
        img  = Image.open(path).convert("RGBA")
        w, h = img.size
        side = min(w, h)
        img  = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
        img  = img.resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        return img

    # ── Card top (background + padding) ──
    st.markdown("""
    <div class="pc" style="padding-bottom:8px;">
      <div style="height:8px;"></div>
    """, unsafe_allow_html=True)

    # ── Photo via st.image (always works in Streamlit) ──
    if os.path.exists(PHOTO_PATH):
        circle_img = make_circle_img(PHOTO_PATH)
        # Centre the image with columns trick
        img_l, img_c, img_r = st.columns([1, 2, 1])
        with img_c:
            st.image(circle_img, width=130)
    else:
        st.markdown("""
        <div style="text-align:center;font-size:70px;margin:10px 0 18px;">👤</div>
        """, unsafe_allow_html=True)

    # ── Card bottom (name / role / button) ──
    st.markdown(f"""
      <div class="pc-name" style="margin-top:4px;">{YOUR_NAME}</div>
      <div class="pc-role"><span>ML Engineer</span><span>Healthcare AI</span></div>
      <a class="li-btn" href="{LINKEDIN_URL}", target="_blank">🔗 &nbsp; View LinkedIn</a>
      <div class="pc-tag">✦ Creator of Healix AI</div>
    </div>
    """, unsafe_allow_html=True)

# ---- ANALYSIS SECTION ----
st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown("""
<div class="ah">
  <div class="ah-icon">🩺</div>
  <div>
    <div class="ah-title">Symptom Analysis</div>
    <div class="ah-desc">Describe your symptoms in plain English. Separate multiple symptoms with commas for best results.</div>
  </div>
</div>
""", unsafe_allow_html=True)

symptoms = st.text_area("Symptoms", placeholder="e.g. fever, headache, chest pain, fatigue, shortness of breath...", height=125, label_visibility="collapsed")

st.markdown("""
<div class="tips-lbl">💡 Quick examples — click to copy</div>
<div class="tips-row">
  <span class="tip">fever, chills, muscle aches, fatigue</span>
  <span class="tip">joint pain, swelling, stiffness</span>
  <span class="tip">wheezing, chest tightness, shortness of breath</span>
  <span class="tip">nausea, vomiting, abdominal cramps</span>
</div>
""", unsafe_allow_html=True)

analyze = st.button("🔍  Analyze Symptoms", use_container_width=True)

# ---- API + RESULTS ----
if analyze:
    if not symptoms.strip():
        st.error("⚠️ Please enter at least one symptom before analyzing.")
    else:
        with st.spinner("Analyzing with NLP engine…"):
            try:
                resp = requests.post(BACKEND_URL, json={"text": symptoms}, timeout=60)

                if resp.status_code == 200:
                    d          = resp.json()
                    disease    = d["disease"]
                    confidence = d["confidence"]
                    cleaned    = d["cleaned_text"]
                    top3       = d["top3"]

                    st.markdown('<hr class="divider">', unsafe_allow_html=True)

                    # Primary card
                    pct = min(confidence, 100)
                    st.markdown(f"""
                    <div class="rp">
                      <div class="rp-lbl">Most Likely Condition</div>
                      <div class="rp-name">{disease}</div>
                      <div class="conf-bar"><div class="conf-fill" style="width:{pct}%;"></div></div>
                      <div class="conf-num">{confidence:.1f}%</div>
                      <div class="conf-sub">Confidence Score</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── TOP PREDICTIONS (rank 1 gets hero card, ranks 2-3 side by side) ──
                    st.markdown("""
                    <div class="rs" style="margin-bottom:0;">
                      <div class="st-lbl">🏆 Top Predictions</div>
                      <div class="st-sub">All possible conditions ranked by model confidence</div>
                    </div>
                    """, unsafe_allow_html=True)

                    rank_colors  = ["#2e7d32", "#558b2f", "#795548"]
                    rank_labels  = ["🥇 Most Likely", "🥈 Second", "🥉 Third"]
                    rank_borders = ["#a5d6a7", "#c5e1a5", "#d7ccc8"]

                    padded_top3 = list(top3) + [None] * (3 - len(top3))
                    cols = st.columns(3, gap="small")
                    for i, col in enumerate(cols):
                        with col:
                            item = padded_top3[i]
                            if item:
                                pct_bar = min(float(item['confidence']), 100)
                                label   = rank_labels[i] if i < len(rank_labels) else f"#{i+1}"
                                bcol    = rank_colors[i]
                                bord    = rank_borders[i]
                                st.markdown(f"""
                                <div style="
                                    background:#fff;
                                    border:2px solid {bord};
                                    border-radius:16px;
                                    padding:20px 18px 18px;
                                    text-align:center;
                                ">
                                  <div style="font-size:11px;font-weight:700;color:{bcol};
                                              text-transform:uppercase;letter-spacing:1.2px;
                                              margin-bottom:10px;">{label}</div>
                                  <div style="font-family:'DM Serif Display',serif;
                                              font-size:20px;color:#1a3d1e;
                                              margin-bottom:14px;word-break:break-word;">
                                    {item['disease'].title()}
                                  </div>
                                  <div style="background:#f0f5ee;border-radius:99px;
                                              height:7px;margin-bottom:10px;overflow:hidden;">
                                    <div style="width:{pct_bar}%;height:100%;
                                                border-radius:99px;
                                                background:linear-gradient(90deg,{bcol},{bcol}99);"></div>
                                  </div>
                                  <div style="font-size:30px;font-weight:800;color:{bcol};">
                                    {item['confidence']}%
                                  </div>
                                  <div style="font-size:11px;color:#8aab8e;margin-top:3px;">
                                    confidence
                                  </div>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div style="
                                    background:#fafafa;
                                    border:2px dashed #ddeeda;
                                    border-radius:16px;
                                    padding:40px 18px;
                                    text-align:center;
                                    color:#ccc;
                                    font-size:13px;
                                ">—</div>
                                """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── ALSO CONSIDER section (items beyond top3 OR synthesised from top3 slots 2-3) ──
                    # Collect candidates: first use any extra predictions beyond top3,
                    # then fall back to top3 slots 1 and 2 (indices 1, 2) if they exist.
                    also_candidates = []
                    if "all_predictions" in d:          # backend may return extended list
                        also_candidates = d["all_predictions"][3:5]
                    if len(also_candidates) < 2:        # fill from top3 slots 1 & 2
                        for item in top3[1:]:
                            if item not in also_candidates:
                                also_candidates.append(item)
                            if len(also_candidates) == 2:
                                break

                    if also_candidates:
                        st.markdown("""
                        <div style="
                            background:#fffbee;
                            border:1.5px solid #f0d060;
                            border-radius:20px;
                            padding:22px 26px 18px;
                            margin-bottom:14px;
                        ">
                          <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                            <span style="font-size:20px;">🔍</span>
                            <div>
                              <div style="font-family:'DM Serif Display',serif;font-size:20px;
                                          color:#7a5800;letter-spacing:-.3px;">
                                Also Consider
                              </div>
                              <div style="font-size:12.5px;color:#9a7800;margin-top:1px;">
                                These conditions share similar symptom patterns — lower probability
                                but worth being aware of
                              </div>
                            </div>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

                        also_cols = st.columns(len(also_candidates), gap="small")
                        for i, (col, item) in enumerate(zip(also_cols, also_candidates)):
                            with col:
                                pct_val  = float(item['confidence'])
                                pct_bar  = min(pct_val, 100)
                                # Amber warning palette
                                bar_col  = "#e6a817" if i == 0 else "#d4894a"
                                bord_col = "#f0d060" if i == 0 else "#f0c090"
                                icon     = "⚠️" if i == 0 else "💭"
                                st.markdown(f"""
                                <div style="
                                    background:#fff;
                                    border:2px solid {bord_col};
                                    border-radius:16px;
                                    padding:20px 18px;
                                    text-align:center;
                                ">
                                  <div style="font-size:22px;margin-bottom:8px;">{icon}</div>
                                  <div style="font-size:10px;font-weight:700;color:#9a7200;
                                              text-transform:uppercase;letter-spacing:1.2px;
                                              margin-bottom:9px;">Low Possibility</div>
                                  <div style="font-family:'DM Serif Display',serif;
                                              font-size:19px;color:#4a3000;
                                              margin-bottom:13px;word-break:break-word;">
                                    {item['disease'].title()}
                                  </div>
                                  <div style="background:#fef9e7;border-radius:99px;
                                              height:7px;margin-bottom:10px;overflow:hidden;">
                                    <div style="width:{pct_bar}%;height:100%;border-radius:99px;
                                                background:linear-gradient(90deg,{bar_col},{bar_col}bb);">
                                    </div>
                                  </div>
                                  <div style="font-size:26px;font-weight:800;color:{bar_col};">
                                    {pct_val:.1f}%
                                  </div>
                                  <div style="font-size:11px;color:#b89040;margin-top:2px;">
                                    probability
                                  </div>
                                  <div style="margin-top:12px;font-size:11.5px;color:#9a7800;
                                              background:#fef9e7;border-radius:8px;padding:7px 10px;
                                              line-height:1.5;">
                                    Consult a doctor if symptoms persist
                                  </div>
                                </div>
                                """, unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)

                    # Cleaned input
                    st.markdown(f"""
                    <div class="rs">
                      <div class="st-lbl">🔤 Processed Input</div>
                      <div class="st-sub">NLP-cleaned symptom text passed to the model</div>
                      <div class="cleaned">{cleaned}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── SHAP / Confidence Breakdown ──────────────────────────
                    has_shap = "shap_features" in d and d.get("shap_features")

                    st.markdown("""
                    <div class="rs" style="margin-bottom:0;">
                      <div class="st-lbl">💡 Feature Importance</div>
                      <div class="st-sub">Which symptoms most influenced the prediction</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if has_shap:
                        # Real SHAP values from backend
                        feats  = d["shap_features"]
                        vals   = d["shap_values"]
                        colors = ["#2e7d32" if v > 0 else "#e53935" for v in vals]
                        x_label = "SHAP Value (positive = increases likelihood)"
                        show_vline = True
                        chart_title = "SHAP Feature Attribution"
                        legend_patches = [
                            mpatches.Patch(color="#2e7d32", label="Increases likelihood"),
                            mpatches.Patch(color="#e53935", label="Decreases likelihood"),
                        ]
                    else:
                        # Fallback: use top3 confidence scores as a horizontal bar chart
                        feats  = [item["disease"].title() for item in top3]
                        vals   = [float(item["confidence"]) for item in top3]
                        # Gradient green shades: brightest = most confident
                        palette = ["#2e7d32", "#558b2f", "#8d6e63"]
                        colors  = palette[:len(feats)]
                        x_label = "Model Confidence (%)"
                        show_vline = False
                        chart_title = "Confidence by Condition (SHAP unavailable)"
                        legend_patches = []

                    n_bars = max(len(feats), 2)
                    fig, ax = plt.subplots(figsize=(9, max(3.2, n_bars * 0.72)))
                    fig.patch.set_facecolor("#ffffff")
                    ax.set_facecolor("#f8faf7")

                    bars = ax.barh(feats, vals, color=colors, height=0.52,
                                   edgecolor="none", zorder=3)

                    # Value labels on each bar
                    for bar, val in zip(bars, vals):
                        label = f"{val:+.3f}" if has_shap else f"{val:.1f}%"
                        ax.text(
                            bar.get_width() + (0.002 if has_shap else 0.3),
                            bar.get_y() + bar.get_height() / 2,
                            label,
                            va="center", ha="left",
                            fontsize=10, color="#3a5e40", fontweight="600"
                        )

                    if show_vline:
                        ax.axvline(0, color="#bbb", linewidth=1.2, zorder=2)

                    ax.set_xlabel(x_label, fontsize=11, color="#5a7a5e", labelpad=10)
                    ax.set_title(chart_title, fontsize=12, color="#1a3d1e",
                                 fontweight="600", pad=12, loc="left")
                    ax.tick_params(colors="#4a6a4e", labelsize=10)
                    for spine in ax.spines.values():
                        spine.set_visible(False)
                    ax.grid(axis="x", color="#e0ede0", linewidth=0.8, zorder=1, linestyle="--")
                    ax.invert_yaxis()   # highest confidence at top

                    if legend_patches:
                        ax.legend(handles=legend_patches, fontsize=10,
                                  frameon=False, loc="lower right")

                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)

                    if not has_shap:
                        st.caption(
                            "ℹ️ SHAP values were not returned by the backend for this prediction. "
                            "The chart above shows raw model confidence scores instead."
                        )

                else:
                    st.error(f"⚠️ Backend error: HTTP {resp.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot reach backend at `http://127.0.0.1:8000`. Make sure FastAPI is running.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")

# ---- DISCLAIMER ----
st.markdown("""
<div class="disc">
  <div class="disc-icon">⚠️</div>
  <div>
    <div class="disc-title">Educational Purposes Only</div>
    <div class="disc-body">
      Healix AI is trained on a <strong>synthetic dataset</strong> and built strictly for
      <strong>educational and demonstration purposes</strong>.
      It must <strong>NOT</strong> be considered a real medical diagnosis.
      Always consult a qualified healthcare professional for medical advice.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---- FOOTER ----
st.markdown(f"""
<div class="ft">
  Powered by <a href="{LINKEDIN_URL}" target="_blank">Healix AI</a>
  &nbsp;·&nbsp; AI-Powered Health Insights
  &nbsp;·&nbsp; For educational use only
</div>
""", unsafe_allow_html=True)
# ── Card bottom (name / role / button) ──