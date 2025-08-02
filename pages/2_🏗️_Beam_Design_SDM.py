import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Beam Design SDM - PyCBA",
    page_icon="🏗️",
    layout="wide"
)

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("🏠 กลับหน้าแรก"):
        st.switch_page("home.py")

with col2:
    st.markdown("<h2 style='text-align: center;'>🏗️ Beam Design - SDM</h2>", unsafe_allow_html=True)

with col3:
    st.markdown("<p style='text-align: center; color: #666;'>PyCBA Suite</p>", unsafe_allow_html=True)

st.markdown("---")

# App description and redirect
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%); color: white; border-radius: 15px; margin: 2rem 0;">
    <h1>🏗️ Beam Design - SDM</h1>
    <h3>โปรแกรมออกแบบคานคอนกรีต</h3>
    <p style="font-size: 1.2em; margin: 2rem 0;">
        ออกแบบคานคอนกรีตเสริมเหล็กตาม Strength Design Method<br>
        คำนวณ Moment Capacity, Steel Reinforcement และ Shear Design
    </p>
</div>
""", unsafe_allow_html=True)

# External app link
st.markdown("## 🌐 เปิดใช้งานโปรแกรม")

st.markdown("""
<div style="background: #f8f9fa; padding: 2rem; border-radius: 10px; border-left: 4px solid #FF6B35;">
    <p style="font-size: 1.1em; margin-bottom: 1rem;">
        <strong>โปรแกรมนี้ถูก Host แยกต่างหากเพื่อประสิทธิภาพสูงสุด</strong>
    </p>
    <p>คลิกปุ่มด้านล่างเพื่อเปิดโปรแกรมในแท็บใหม่:</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <a href="https://beam-design-sdm-app.streamlit.app/" target="_blank" 
           style="background: linear-gradient(45deg, #FF6B35, #F7931E); 
                  color: white; 
                  padding: 1rem 3rem; 
                  border: none; 
                  border-radius: 25px; 
                  font-size: 1.2rem; 
                  font-weight: bold; 
                  text-decoration: none; 
                  display: inline-block; 
                  box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
                  transition: all 0.3s ease;">
            🚀 เปิด Beam Design SDM
        </a>
    </div>
    
    <style>
    a:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 107, 53, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# App features
st.markdown("## 🔧 คุณสมบัติของโปรแกรม")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📊 การออกแบบโมเมนต์
    - คำนวณ Moment Capacity
    - ออกแบบ Flexural Reinforcement
    - ตรวจสอบ Steel Ratio (ρ)
    - คำนวณ Balanced Steel Ratio
    - ตรวจสอบ Over/Under Reinforced
    """)

with col2:
    st.markdown("""
    ### ⚡ การออกแบบแรงเฉือน
    - คำนวณ Shear Capacity (Vc)
    - ออกแบบ Shear Reinforcement
    - คำนวณระยะห่างของ Stirrups
    - ตรวจสอบ Maximum Shear
    - Minimum Shear Reinforcement
    """)

with col3:
    st.markdown("""
    ### 📏 การตรวจสอบการโก่งตัว
    - คำนวณ Moment of Inertia
    - ตรวจสอบ Deflection Limit
    - คำนวณ Long-term Deflection
    - ตรวจสอบ Serviceability
    - Cracking Moment Analysis
    """)

# Embed option
st.markdown("---")
st.markdown("## 📱 หรือใช้งานผ่าน Embed (อาจโหลดช้า)")

if st.button("🔄 โหลดโปรแกรมในหน้านี้"):
    with st.spinner("กำลังโหลดโปรแกรม..."):
        st.components.v1.iframe(
            src="https://beam-design-sdm-app.streamlit.app/?embed=true",
            height=800,
            scrolling=True
        )

# Manual/Guide
st.markdown("---")
st.markdown("## 📚 วิธีการใช้งาน")

with st.expander("📋 ขั้นตอนการใช้งาน"):
    st.markdown("""
    ### ขั้นตอนที่ 1: กำหนดข้อมูลคาน
    1. กรอกขนาดหน้าตัดคาน (b, h, d)
    2. กำหนดคุณสมบัติวัสดุ (f'c, fy)
    3. ระบุความยาวคานและการรองรับ
    
    ### ขั้นตอนที่ 2: กำหนดน้ำหนักบรรทุก
    1. Dead Load (DL)
    2. Live Load (LL)
    3. โปรแกรมจะคำนวณ Factored Load อัตโนมัติ
    
    ### ขั้นตอนที่ 3: ดูผลการออกแบบ
    1. Steel Reinforcement ที่ต้องการ
    2. จำนวนและขนาดเหล็กเส้น
    3. ระยะห่าง Stirrups
    4. การตรวจสอบ Deflection
    """)

st.info("💡 โปรแกรมนี้เหมาะสำหรับวิศวกรโครงสร้างที่ต้องการออกแบบคานคอนกรีตเสริมเหล็กตามมาตรฐาน ACI 318 และ มยผ. 1311")
