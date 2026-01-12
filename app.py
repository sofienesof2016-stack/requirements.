import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io

# --- 1. الإعدادات وإدارة الحالة ---
st.set_page_config(page_title="منصة تيسير | TAYSIR 2026", layout="wide")

# تهيئة المتغيرات في الجلسة (Session State)
if 'page' not in st.session_state: st.session_state.page = "home"
if 'logged_user' not in st.session_state: st.session_state.logged_user = None
if 'inventories' not in st.session_state: st.session_state.inventories = {}
if 'public_products' not in st.session_state:
    st.session_state.public_products = [
        {"name": "زيت زيتون بكر", "owner": "سفيان الزوابي", "price": "25.000",
         "image": "https://cdn-icons-png.flaticon.com/512/1154/1154448.png"},
        {"name": "عسل نحل جبلي", "owner": "مناحل الشمال", "price": "45.000",
         "image": "https://cdn-icons-png.flaticon.com/512/2154/2154316.png"},
    ]

# --- 2. التنسيق الجمالي الاحترافي (Olive & Navy) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }

    /* الهيدر العلوي الفخم */
    .hero-section {
        background: linear-gradient(135deg, #3d4b26 0%, #556b2f 100%);
        padding: 50px 20px;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    .hero-section h1 { color: white !important; font-size: 3.5rem !important; margin: 0; }
    .hero-section p { color: #f0f0f0 !important; font-size: 1.2rem; opacity: 0.9; }

    /* الأزرار باللون الأزرق البحري */
    .stButton>button {
        background-color: #1a3a5f !important; /* Navy Blue */
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        transition: 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #244d7d !important;
        transform: translateY(-2px);
    }

    /* بطاقات العرض */
    .product-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #eee;
        text-align: center;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .product-card:hover { box-shadow: 0 12px 25px rgba(0,0,0,0.07); }

    /* جداول المخزن */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 15px;
        overflow: hidden;
        margin-top: 15px;
    }
    .styled-table th { background-color: #556b2f; color: white; padding: 15px; text-align: center; }
    .styled-table td { background-color: white; padding: 12px; border-bottom: 1px solid #f2f2f2; text-align: center; }

    /* أيقونات التواصل */
    .header-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 40px;
        background: white;
        border-bottom: 2px solid #556b2f;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. الشريط العلوي العلوي ---
st.markdown(f"""
    <div class="header-nav">
        <div style="display: flex; gap: 15px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" width="25">
            <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="25">
        </div>
        <div style="font-weight:bold; color:#1a3a5f;">👤 متصل الآن: {st.session_state.logged_user if st.session_state.logged_user else "زائر"}</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. واجهة الترحيب (Hero Section) ---
st.markdown(f"""
    <div class="hero-section">
        <h1>تيسير | TAYSIR</h1>
        <p>حلول أسهل.. قرارات أذكى</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#556b2f;'>🛠️ بوابة التحكم</h2>", unsafe_allow_html=True)
    st.write("---")
    if st.button("🏠 المعرض العام"): st.session_state.page = "home"
    if st.button("📊 المحاكاة المالية"): st.session_state.page = "simulation"
    if st.button("📦 إدارة المخزن"): st.session_state.page = "stock"
    if st.button("➕ إضافة عرض بيع"): st.session_state.page = "quick_add"

    if st.session_state.logged_user:
        st.write("---")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.logged_user = None;
            st.rerun()

# --- 6. منطق الصفحات ---

# الصفحة الرئيسية
if st.session_state.page == "home":
    st.markdown("### 🏛️ المنتجات المتاحة")
    cols = st.columns(3)
    for i, prod in enumerate(st.session_state.public_products):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="product-card">
                    <h4 style="color:#1a3a5f;">{prod['name']}</h4>
                    <p style="font-size:0.8rem; color:gray;">التاجر: {prod['owner']}</p>
                    <h2 style="color:#556b2f;">{prod['price']} <small style="font-size:12px;">د.ت</small></h2>
                </div>
            """, unsafe_allow_html=True)
            # عرض الصور إذا كانت رابطاً أو كائناً
            if isinstance(prod['image'], str):
                st.image(prod['image'], use_container_width=True)
            else:
                st.image(prod['image'], use_container_width=True)
            st.button("شراء الآن", key=f"buy_{i}")

# صفحة المحاكاة المالية (Logic الفعلي)
elif st.session_state.page == "simulation":
    st.markdown("### 📊 دراسة الجدوى والمحاكاة الذكية")
    with st.container():
        col_in, col_res = st.columns([1, 1.2])
        with col_in:
            st.info("مدخلات المشروع")
            capital = st.number_input("رأس المال المخصص (د.ت)", value=10000)
            fixed_costs = st.number_input("المصاريف القارة", value=600)
            labor_costs = st.number_input("مصاريف العمالة", value=800)
            unit_cost = st.number_input("تكلفة الوحدة", value=12.0)
            unit_price = st.number_input("سعر البيع", value=20.0)
            sales_target = st.slider("المبيعات الشهرية", 10, 2000, 200)
            run_sim = st.button("🚀 بدء محاكاة الأرباح")

        with col_res:
            if run_sim:
                # الحسابات البرمجية
                total_fixed = fixed_costs + labor_costs
                profit_per_unit = unit_price - unit_cost
                revenue = sales_target * unit_price
                monthly_profit = (sales_target * profit_per_unit) - total_fixed
                roi = (monthly_profit * 12 / capital) * 100 if capital > 0 else 0

                st.markdown("#### 📈 النتائج")
                st.metric("صافي الربح الشهري", f"{monthly_profit:,.0f} د.ت")
                st.metric("العائد السنوي المتوقع", f"{roi:.1f} %")

                chart_data = pd.DataFrame({
                    'الفئة': ['التكاليف', 'الأرباح'],
                    'المبلغ': [total_fixed + (unit_cost * sales_target), max(0, monthly_profit)]
                })
                st.bar_chart(chart_data.set_index('الفئة'))
            else:
                st.warning("أدخل البيانات واضغط على الزر لبدء التحليل.")

# صفحة المخزن (Logic الإضافة والحذف)
elif st.session_state.page == "stock":
    if not st.session_state.logged_user:
        st.subheader("🔐 الدخول لإدارة مخزنك")
        name_input = st.text_input("اسم التاجر")
        if st.button("دخول"):
            st.session_state.logged_user = name_input
            if name_input not in st.session_state.inventories:
                st.session_state.inventories[name_input] = []
            st.rerun()
    else:
        st.subheader(f"📦 مخزن: {st.session_state.logged_user}")
        inv = st.session_state.inventories[st.session_state.logged_user]

        with st.expander("➕ إضافة سلعة للمخزن"):
            c1, c2, c3 = st.columns(3)
            in_name = c1.text_input("المنتج")
            in_buy = c2.number_input("سعر الشراء", min_value=0.0)
            in_qty = c3.number_input("الكمية", min_value=1)
            if st.button("حفظ في القاعدة"):
                inv.append({"المنتج": in_name, "شراء": in_buy, "الكمية": in_qty})
                st.success("تم الحفظ")
                st.rerun()

        if inv:
            # عرض الجدول بتنسيق CSS مخصص
            df = pd.DataFrame(inv)
            st.table(df)

            st.markdown("#### 🛒 تحديث مبيعات")
            p_sell = st.selectbox("اختر المنتج المباع", [item['المنتج'] for item in inv])
            q_sell = st.number_input("الكمية المباعة", min_value=1)
            if st.button("📦 تحديث المخزون"):
                for item in inv:
                    if item['المنتج'] == p_sell and item['الكمية'] >= q_sell:
                        item['الكمية'] -= q_sell
                        st.success("تم التحديث بنجاح")
                        st.rerun()
        else:
            st.info("مخزنك فارغ حالياً.")

# صفحة الإضافة السريعة للموقع
elif st.session_state.page == "quick_add":
    st.subheader("➕ إضافة عرض بيع جديد للمعرض")
    with st.form("quick_form"):
        qn = st.text_input("اسم المنتج المعروض")
        qp = st.text_input("السعر المعروض")
        file = st.file_uploader("صورة المنتج", type=['jpg', 'png'])
        submit = st.form_submit_button("🚀 نشر العرض الآن")

        if submit and qn and file:
            img = Image.open(file)
            st.session_state.public_products.append({
                "name": qn,
                "owner": st.session_state.logged_user if st.session_state.logged_user else "زائر محترف",
                "price": qp,
                "image": img
            })
            st.success("تم النشر بنجاح!")
            st.session_state.page = "home"
            st.rerun()

# التذييل
st.markdown(
    "<br><hr><p style='text-align:center; color:gray;'>منصة تيسير © 2026 - الملكية الفكرية للسيد سفيان الزوابي</p>",
    unsafe_allow_html=True)
