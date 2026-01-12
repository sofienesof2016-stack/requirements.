import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="TAYSIR 2026", layout="wide")

# CSS لإخفاء الهيدر الافتراضي وحل مشكلة الصورة 35
st.markdown("""
    <style>
    [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
    .main-title {
        background-color: #556b2f !important;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        color: white !important;
    }
    </style>
    <div class="main-title">
        <h1>تيسير | TAYSIR</h1>
        <p>حلول أسهل.. قرارات أذكى</p>
    </div>
""", unsafe_allow_html=True)
