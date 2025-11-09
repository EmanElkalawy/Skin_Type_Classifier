# skin_app.py — Professional Version with Auto-Model Download
import streamlit as st
from PIL import Image
import requests
import io
import os
import gdown
import time

# ----------------------------
# Configuration
# ----------------------------
MODEL_URL = "https://drive.google.com/file/d/1Go1ZAJAXN9Lpf-xUztm7_JZE27I6SZ18/view?usp=drive_link"  
API_URL = "http://127.0.0.1:8000/classify_skin"  

st.set_page_config(page_title="Skin Type Classifier", page_icon="🧴", layout="centered")

# ----------------------------
# Skin Info (for display)
# ----------------------------
SKIN_INFO = {
    'dry': {'color': '#1E90FF', 'advice': 'Focus on hydration and gentle, oil-based moisturizers.'},
    'normal': {'color': '#3CB371', 'advice': 'Maintain your routine! Use light, antioxidant-rich products.'},
    'oily': {'color': '#FFD700', 'advice': 'Use non-comedogenic products and gentle exfoliants to manage shine.'},
    'sensitive': {'color': '#FA8072', 'advice': 'Avoid harsh chemicals and fragrances. Introduce new products slowly.'},
    'unknown': {'color': '#A9A9A9', 'advice': 'Analysis inconclusive. Try uploading a clearer, well-lit image.'}
}
FALLBACK_INFO = SKIN_INFO['unknown']

# ----------------------------
# Ensure saved_model folder and download model if missing
# ----------------------------
os.makedirs("saved_model", exist_ok=True)
if not os.path.exists(MODEL_PATH):
    st.info("Downloading pre-trained model...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# ----------------------------
# CSS Styling
# ----------------------------
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f7fbff 0%, #ffffff 100%);
    }
    .block-container { max-width: 820px; padding-top: 28px; }
    .header-card {
        background: white;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 8px 30px rgba(13, 38, 88, 0.06);
        margin-bottom: 24px;
    }
    .title { color: #0b3d91; font-weight: 700; font-size: 28px; text-align: center; }
    .subtitle { color: #556677; font-size: 14px; text-align: center; margin-bottom: 8px; }
    .result-card {
        background: linear-gradient(180deg, #ffffff, #f3f9ff);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 6px 20px rgba(11,61,145,0.06);
        text-align: center;
        margin-top: 15px;
    }
    .result-prediction { font-weight: 800; font-size: 32px; margin-bottom: 5px; }
    .result-advice { color: #556677; margin-top: 15px; font-size: 16px; }
    .stProgress { margin-top: 5px; }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown('<div class="header-card">', unsafe_allow_html=True)
st.markdown('<div class="title">Skin Type Classifier AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload or capture a clear skin image for analysis using the trained model.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Image Upload / Camera Input
# ----------------------------
st.subheader("📸 Choose Image Source")
option = st.radio("Select input method:", ["Upload Image", "Use Camera"], horizontal=True)

uploaded_file = None
if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload Image (JPG / PNG)", type=["jpg", "jpeg", "png"])
elif option == "Use Camera":
    uploaded_file = st.camera_input("Take a photo")

if uploaded_file is None:
    st.info("Please upload or capture an image to get a prediction.")
    st.stop()

# Read and display the image
try:
    image = Image.open(io.BytesIO(uploaded_file.getvalue())).convert("RGB")
except Exception:
    st.error("Unable to process the image. Try again with a valid file.")
    st.stop()

st.image(image, caption="Selected Image", use_container_width=True)

# ----------------------------
# Send to FastAPI for Prediction
# ----------------------------
st.markdown("---")
time.sleep(0.5)

with st.spinner("Analyzing image..."):
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or "image/jpeg")}
        resp = requests.post(API_URL, files=files, timeout=45)
    except requests.RequestException:
        st.error(f"❌ Could not connect to API. Ensure FastAPI server is running at {API_URL}.")
        st.stop()

if resp.status_code != 200:
    try:
        err = resp.json().get("error", resp.text)
    except Exception:
        err = resp.text
    st.error(f"❌ Prediction error: {err}")
    st.stop()

result = resp.json()
prediction = result.get("prediction", "unknown").lower()
confidence_str = result.get("confidence", "0%")

# Extract numeric confidence
try:
    conf_val = float(confidence_str.strip().strip("%"))
except Exception:
    conf_val = 0.0

info = SKIN_INFO.get(prediction, FALLBACK_INFO)

# ----------------------------
# Display Result
# ----------------------------
st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.markdown(
    f"<h2 class='result-prediction' style='color:{info['color']};'>{prediction.upper()}</h2>",
    unsafe_allow_html=True,
)
st.markdown(f"<p>Confidence: <b>{conf_val:.2f}%</b></p>", unsafe_allow_html=True)
st.progress(min(conf_val / 100, 1.0))
st.markdown(f"<p class='result-advice'><b>Recommendation:</b> {info['advice']}</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 Skin AI — Powered by PyTorch, Streamlit & FastAPI")
