import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Bridge Analysis - PyCBA",
    page_icon="🌉",
    layout="wide"
)

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("🏠 กลับหน้าแรก"):
        st.switch_page("home.py")

with col2:
    st.markdown("<h2 style='text-align: center;'>🌉 Bridge Analysis</h2>", unsafe_allow_html=True)

with col3:
    st.markdown("<p style='text-align: center; color: #666;'>PyCBA Suite</p>", unsafe_allow_html=True)

st.markdown("---")

# Coming Soon Message
st.markdown("""
<div style="text-align: center; padding: 3rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin: 2rem 0;">
    <h1>🚧 กำลังพัฒนา</h1>
    <h3>Bridge Analysis Module</h3>
    <p style="font-size: 1.2em; margin: 2rem 0;">
        โมดูลวิเคราะห์สะพานและโครงสร้างขนาดใหญ่<br>
        อยู่ในระหว่างการพัฒนา คาดว่าจะเสร็จในปลายปี 2025
    </p>
</div>
""", unsafe_allow_html=True)

# Quick navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("🏗️ Continuous Beam Analysis"):
        st.switch_page("pages/1_🏗️_Continuous_Beam_Analysis.py")

with col2:
    if st.button("🏗️ Beam Design SDM"):
        st.switch_page("pages/2_🏗️_Beam_Design_SDM.py")
