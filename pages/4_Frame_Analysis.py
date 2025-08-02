import streamlit as st

# Page configuration
st.set_page_config(
    page_title="🏢 Frame Analysis - PyCBA",
    page_icon="🏢",
    layout="wide"
)

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("🏠 กลับหน้าแรก"):
        st.switch_page("home.py")

with col2:
    st.markdown("<h2 style='text-align: center;'>🏢 Frame Analysis</h2>", unsafe_allow_html=True)

with col3:
    st.markdown("<p style='text-align: center; color: #666;'>PyCBA Suite</p>", unsafe_allow_html=True)

st.markdown("---")

# Coming Soon Message
st.markdown("""
<div style="text-align: center; padding: 3rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin: 2rem 0;">
    <h1>📅 วางแผนพัฒนา</h1>
    <h3>Frame Analysis Module</h3>
    <p style="font-size: 1.2em; margin: 2rem 0;">
        โมดูลวิเคราะห์โครงข้อแข็งสำหรับอาคาร<br>
        อยู่ในระหว่างการวางแผนและออกแบบ<br>
        คาดว่าจะเริ่มพัฒนาในปี 2026
    </p>
</div>
""", unsafe_allow_html=True)

# Quick navigation
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏗️ Continuous Beam"):
        st.switch_page("pages/1_🏗️_Continuous_Beam_Analysis.py")

with col2:
    if st.button("🏗️ Beam Design"):
        st.switch_page("pages/2_🏗️_Beam_Design_SDM.py")

with col3:
    if st.button("🌉 Bridge Analysis"):
        st.switch_page("pages/3_🌉_Bridge_Analysis.py")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>PyCBA Suite - Frame Analysis Module (Coming 2026)</p>", 
    unsafe_allow_html=True
)
