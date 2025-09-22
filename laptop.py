import streamlit as st
import joblib
import pandas as pd
import math
from streamlit_lottie import st_lottie
import json
import requests
import time


# تحسين الأداء عن طريق التخزين المؤقت للنموذج
@st.cache_resource
def load_model():
    return joblib.load('laptop_random_forest_model.pkl')


@st.cache_resource
def load_scaler():
    return joblib.load('laptop_scaler.pkl')


# تهيئة الصفحة
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# تحميل النموذج والمقياس
model = load_model()
scaler = load_scaler()


# إضافة أنيميشن للخلفية مع ألوان بنفسجية
st.markdown("""
<style>
    /* أنيميشن للخلفية */
    @keyframes move {
        100% {
            transform: translate3d(0, 0, 1px) rotate(360deg);
        }
    }
    
    .background {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        background: #ffffff;
        overflow: hidden;
        z-index: -1;
    }
    
    .background span {
        width: 20vmin;
        height: 20vmin;
        border-radius: 20vmin;
        backface-visibility: hidden;
        position: absolute;
        animation: move;
        animation-duration: 45s;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
    }
    
    .background span:nth-child(1) {
        color: #6a0dad;
        top: 15%;
        left: 72%;
        animation-duration: 36s;
        animation-delay: -3s;
        transform-origin: -4vw 3vh;
        box-shadow: 40vmin 0 5.447481430512199vmin currentColor;
    }
    
    .background span:nth-child(2) {
        color: #4b0082;
        top: 80%;
        left: 32%;
        animation-duration: 42s;
        animation-delay: -27s;
        transform-origin: 4vw 21vh;
        box-shadow: 40vmin 0 5.894942552383647vmin currentColor;
    }
    
    .background span:nth-child(3) {
        color: #c58cff;
        top: 32%;
        left: 12%;
        animation-duration: 38s;
        animation-delay: -15s;
        transform-origin: 1vw 0vh;
        box-shadow: -40vmin 0 5.259032930041024vmin currentColor;
    }
    
    /* تصميم البطاقة العائمة */
    .floating-card {
        position: sticky;
        top: 20px;
        background: linear-gradient(135deg, #F8F9F9 0%, #E8EAED 100%);
        padding: 30px 20px 25px 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(20,20,20,0.16);
        min-width: 240px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid #6a0dad;
        z-index: 999;
        margin-bottom: 20px;
    }
    
    .floating-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(20,20,20,0.2);
    }
    
    /* تحسينات عامة للأداء */
    .stSelectbox, .stSlider, .stCheckbox, .stNumberInput {
        transition: all 0.3s ease;
    }
    
    /* تحسينات للخطوط */
    h1, h2, h3, .stSelectbox label, .stSlider label, .stCheckbox label {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* إزالة التمرير غير الضروري */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# إضافة أنيميشن الخلفية
st.markdown("""
<div class="background">
    <span></span>
    <span></span>
    <span></span>
</div>
""", unsafe_allow_html=True)


# Logo or image
st.image("logo.png", width=120)  # Replace with your desired image file


# Title
col_title1, col_title2, col_title3 = st.columns([1, 2, 1])
with col_title2:
    st.markdown(
        """
        <h1 style="text-align:center; color:#4b0082; font-family:Arial; margin-bottom:10px;">
            Laptop Price Prediction App
        </h1>
        """,
        unsafe_allow_html=True
    )


# --- Dropdown options ---
company_options = ['Dell', 'HP', 'Apple', 'Asus', 'Lenovo', 'Acer']
typename_options = ['Notebook', 'Ultrabook', 'Gaming', '2 in 1', 'Netbook']
cpu_options = ['Intel', 'AMD', 'Other']
gpu_options = ['Nvidia', 'AMD', 'Intel', 'Other']
os_options = ['Windows', 'MacOS', 'Linux', 'Others']


# Resolution choices
resolutions = {
    "1366x768": (1366, 768),
    "1600x900": (1600, 900),
    "1920x1080": (1920, 1080),
    "2560x1440": (2560, 1440),
    "3840x2160": (3840, 2160)
}


inch_options = [13.3, 14, 15.6, 17.3]


# --- Split page into two columns, inputs get 2/3, price gets 1/3 ---
col1, col2 = st.columns([2, 1])


with col1:
    # --- User inputs ---
    st.markdown("### Laptop Specifications")
    
    # استخدام أعمدة متعددة لتحسين التخطيط
    col1_1, col1_2 = st.columns(2)
    
    with col1_1:
        Company = st.selectbox('Company', company_options, key='company')
        TypeName = st.selectbox('Type Name', typename_options, key='typename')
        Cpu_brand = st.selectbox('CPU Brand', cpu_options, key='cpu')
        Gpu_brand = st.selectbox('GPU Brand', gpu_options, key='gpu')
        
    with col1_2:
        os_val = st.selectbox('Operating System', os_options, key='os')
        Ram = st.selectbox('RAM (GB)', [4, 8, 16, 32, 64], key='ram')
        
        # Weight options based on TypeName
        if TypeName == "Gaming":
            weight_options = {"2.0 – 2.5 kg": 2.25, "2.6 – 3.5 kg": 3.0, "3.6 – 5.0 kg": 4.0}
        elif TypeName in ["Ultrabook", "Netbook"]:
            weight_options = {"0.5 – 1.0 kg": 0.75, "1.1 – 1.5 kg": 1.3, "1.6 – 2.0 kg": 1.8}
        else:
            weight_options = {"1.0 – 1.5 kg": 1.3, "1.6 – 2.5 kg": 2.0, "2.6 – 3.5 kg": 3.0}
        Weight = weight_options[st.selectbox('Weight', list(weight_options.keys()), key='weight')]


    # Storage
    st.markdown("#### Storage Configuration")
    col_storage1, col_storage2 = st.columns(2)
    with col_storage1:
        HDD = st.selectbox('HDD (GB)', [128, 256, 512, 1024, 2000], key='hdd')
    with col_storage2:
        SSD = st.selectbox('SSD (GB)', [128, 256, 512, 1024, 2000], key='ssd')


    # Touchscreen toggle
    Touchscreen = 1 if st.checkbox("Touchscreen", key='touch') else 0


    # Resolution & Inches
    st.markdown("#### Display Specifications")
    col_disp1, col_disp2 = st.columns(2)
    with col_disp1:
        res_choice = st.selectbox("Screen Resolution:", list(resolutions.keys()), key='res')
    with col_disp2:
        inch_choice = st.selectbox("Screen Size (Inches):", inch_options, key='inch')
    
    X_res, Y_res = resolutions[res_choice]
    ppi = math.sqrt(X_res**2 + Y_res**2) / inch_choice


    # --- Encoding ---
    company_map = {name: idx for idx, name in enumerate(company_options)}
    typename_map = {name: idx for idx, name in enumerate(typename_options)}
    cpu_map = {name: idx for idx, name in enumerate(cpu_options)}
    gpu_map = {name: idx for idx, name in enumerate(gpu_options)}
    os_map = {name: idx for idx, name in enumerate(os_options)}


    # إنشاء DataFrame للإدخال
    input_dict = {
        'Company': [company_map[Company]],
        'TypeName': [typename_map[TypeName]],
        'Ram': [Ram],
        'Weight': [Weight],
        'Touchscreen': [Touchscreen],
        'IPS': [0],  # Always 0 to avoid confusion in model
        'ppi': [ppi],
        'Cpu_brand': [cpu_map[Cpu_brand]],
        'HDD': [HDD],
        'SSD': [SSD],
        'Gpu_brand': [gpu_map[Gpu_brand]],
        'os': [os_map[os_val]]
    }


    input_df = pd.DataFrame(input_dict)
    input_scaled = scaler.transform(input_df)


    # التنبؤ بالسعر
    price_prediction = model.predict(input_scaled)


with col2:
    # بطاقة السعر العائمة
    st.markdown(
        f"""
        <div class="floating-card">
            <h2 style="color:#6a0dad; font-family:Arial; margin-bottom:18px;">
                Predicted Price
            </h2>
            <h1 style="color:#313638; font-size:2.2em; font-weight:bold; margin:0;">
                💶{price_prediction[0]:,.2f}
            </h1>
            <div style="color:#34495E; margin-top:-6px; font-size:1.13em;">
                Unit Price
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # معلومات إضافية
    st.info("""
    **Note:** This prediction is based on a machine learning model trained on historical laptop data. 
    Actual prices may vary based on market conditions and additional features.
    """)


# إضافة تذييل الصفحة
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #6c757d; padding: 20px;">
        <p>Laptop Price Prediction App © 2026 | Powered by Machine Learning</p>
    </div>
    """,
    unsafe_allow_html=True
)


# تحميل وتنفيذ JavaScript لتحسين الأداء
st.markdown("""
<script>
    // تحسين الأداء عن طريق تأخير تحميل بعض العناصر
    document.addEventListener('DOMContentLoaded', function() {
        // تأخير تحميل العناصر غير الحرجة
        setTimeout(function() {
            // أي عناصر إضافية يمكن تحميلها لاحقًا
        }, 1000);
    });
    
    // جعل البطاقة تتبع التمرير
    window.addEventListener('scroll', function() {
        const card = document.querySelector('.floating-card');
        if (card) {
            // الحفاظ على موضع البطاقة أثناء التمرير
            card.style.top = Math.max(20, window.scrollY - 100) + 'px';
        }
    });
</script>
""", unsafe_allow_html=True)

