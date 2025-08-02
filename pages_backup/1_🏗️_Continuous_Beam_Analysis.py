import streamlit as st
import sys
import os

# Add current directory to path to import advanced_app
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import the main beam analysis app
try:
    from advanced_app import main as beam_analysis_main
    
    # Page configuration
    st.set_page_config(
        page_title="Continuous Beam Analysis - PyCBA",
        page_icon="🏗️",
        layout="wide"
    )
    
    # Navigation back to home
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("🏠 กลับหน้าแรก"):
            st.switch_page("home.py")
    
    with col2:
        st.markdown("<h2 style='text-align: center;'>🏗️ Continuous Beam Analysis</h2>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<p style='text-align: center; color: #666;'>PyCBA Suite</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Run the beam analysis app
    beam_analysis_main()
    
except ImportError as e:
    st.error(f"""
    ⚠️ ไม่สามารถโหลดโปรแกรม Beam Analysis ได้
    
    กรุณาตรวจสอบว่าไฟล์ advanced_app.py อยู่ในโฟลเดอร์หลัก
    
    ข้อผิดพลาด: {e}
    """)
    
    if st.button("🔄 ลองใหม่"):
        st.rerun()
