import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Beam Design - Strength Design Method - PyCBA",
    page_icon="🏗️",
    layout="wide"
)

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("🏠 กลับหน้าแรก"):
        st.switch_page("home.py")

with col2:
    st.markdown("<h2 style='text-align: center;'>🏗️ Beam Design - Strength Design Method</h2>", unsafe_allow_html=True)

with col3:
    st.markdown("<p style='text-align: center; color: #666;'>PyCBA Suite</p>", unsafe_allow_html=True)

st.markdown("---")

# App description and redirect
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%); color: white; border-radius: 15px; margin: 2rem 0;">
    <h1>🏗️ โปรแกรมออกแบบคานคอนกรีต</h1>
    <h3>Strength Design Method (SDM)</h3>
    <p style="font-size: 1.2em; margin: 2rem 0;">
        โปรแกรมออกแบบคานคอนกรีตเสริมเหล็กตามหลักการ Strength Design Method<br>
        คำนวณ Moment Capacity, Steel Reinforcement และ Shear Design
    </p>
</div>
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

# Direct link to the application
st.markdown("---")

# External app integration
st.markdown("## 🌐 เปิดใช้งานโปรแกรม")

st.markdown("""
<div style="background: #f8f9fa; padding: 2rem; border-radius: 10px; border-left: 4px solid #4CAF50;">
    <p style="font-size: 1.1em; margin-bottom: 1rem;">
        <strong>โปรแกรมนี้ถูก Host แยกต่างหากเพื่อประสิทธิภาพสูงสุด</strong>
    </p>
    <p>คลิกปุ่มด้านล่างเพื่อเปิดโปรแกรมในแท็บใหม่:</p>
</div>
""", unsafe_allow_html=True)

# Create columns for centered button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Direct link button with custom styling
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <a href="https://beam-design-sdm-app.streamlit.app/" target="_blank" 
           style="background: linear-gradient(45deg, #4CAF50, #45a049); 
                  color: white; 
                  padding: 1rem 3rem; 
                  border: none; 
                  border-radius: 25px; 
                  font-size: 1.2rem; 
                  font-weight: bold; 
                  text-decoration: none; 
                  display: inline-block; 
                  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
                  transition: all 0.3s ease;">
            🚀 เปิด Beam Design SDM
        </a>
    </div>
    
    <style>
    a:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

# Additional information
st.markdown("---")
st.markdown("## 📚 ข้อมูลเพิ่มเติม")

tab1, tab2, tab3 = st.tabs(["🔬 หลักการทำงาน", "📖 วิธีใช้งาน", "⚙️ Technical Details"])

with tab1:
    st.markdown("""
    ### 🔬 Strength Design Method (SDM)
    
    โปรแกรมนี้ใช้หลักการ **Strength Design Method** หรือ **Ultimate Strength Design** 
    ซึ่งเป็นวิธีการออกแบบที่พิจารณาความแข็งแรงสูงสุดของคาน
    
    #### หลักการสำคัญ:
    - **Load Factors**: ใช้ค่าความปลอดภัยกับน้ำหนักบรรทุก
    - **Resistance Factors**: ใช้ค่าลดกำลังวัสดุ (φ factors)
    - **Ultimate Capacity**: ออกแบบตามกำลังสูงสุด
    - **Compatibility**: ตรวจสอบความเข้ากันได้ของ strain
    
    #### สูตรหลัก:
    ```
    φMn ≥ Mu
    φVn ≥ Vu
    
    Where:
    φ = Resistance factor
    Mn, Vn = Nominal strength
    Mu, Vu = Factored loads
    ```
    """)

with tab2:
    st.markdown("""
    ### 📖 วิธีการใช้งาน
    
    #### ขั้นตอนที่ 1: กำหนดข้อมูลคาน
    1. กรอกขนาดหน้าตัดคาน (b, h, d)
    2. กำหนดคุณสมบัติวัสดุ (f'c, fy)
    3. ระบุความยาวคานและการรองรับ
    
    #### ขั้นตอนที่ 2: กำหนดน้ำหนักบรรทุก
    1. Dead Load (DL)
    2. Live Load (LL)
    3. โปรแกรมจะคำนวณ Factored Load อัตโนมัติ
    
    #### ขั้นตอนที่ 3: ดูผลการออกแบบ
    1. Steel Reinforcement ที่ต้องการ
    2. จำนวนและขนาดเหล็กเส้น
    3. ระยะห่าง Stirrups
    4. การตรวจสอบ Deflection
    
    #### ขั้นตอนที่ 4: ตรวจสอบผลลัพธ์
    1. ตรวจสอบ Steel Ratio
    2. ตรวจสอบความปลอดภัย
    3. ดาวน์โหลดรายงาน
    """)

with tab3:
    st.markdown("""
    ### ⚙️ Technical Specifications
    
    #### รองรับมาตรฐาน:
    - **ACI 318**: American Concrete Institute
    - **มยผ. 1311**: มาตรฐานไทยคอนกรีตเสริมเหล็ก
    - **Eurocode 2**: European Standard (บางส่วน)
    
    #### ขอบเขตการใช้งาน:
    - **ความกว้างคาน**: 200-1000 mm
    - **ความสูงคาน**: 300-1500 mm
    - **ความแข็งแรงคอนกรีต**: 15-50 MPa
    - **ความแข็งแรงเหล็ก**: 240-500 MPa
    
    #### ฟีเจอร์ขั้นสูง:
    - T-beam design
    - Doubly reinforced beam
    - Deep beam analysis
    - Torsion design
    - Prestressed concrete (บางส่วน)
    
    #### Performance:
    - **ความเร็วคำนวณ**: < 2 วินาที
    - **ความแม่นยำ**: ±2% compared to hand calculation
    - **รองรับ Browser**: Chrome, Firefox, Safari, Edge
    """)

# Comparison with other programs
st.markdown("---")
st.markdown("## 🔄 เปรียบเทียบกับโปรแกรมอื่นใน PyCBA Suite")

comparison_data = {
    "โปรแกรม": [
        "Continuous Beam Analysis",
        "Beam Design SDM",
        "Bridge Analysis (วางแผน)",
        "Frame Analysis (วางแผน)"
    ],
    "ประเภท": [
        "Analysis",
        "Design", 
        "Analysis",
        "Analysis & Design"
    ],
    "สถานะ": [
        "✅ พร้อมใช้งาน",
        "✅ พร้อมใช้งาน",
        "🚧 กำลังพัฒนา",
        "📅 วางแผนพัฒนา"
    ],
    "Use Case": [
        "วิเคราะห์คานต่อเนื่อง",
        "ออกแบบคานคอนกรีต",
        "วิเคราะห์สะพาน",
        "วิเคราะห์โครงอาคาร"
    ]
}

st.table(comparison_data)

# Footer with links
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏗️ Continuous Beam Analysis"):
        st.switch_page("pages/1_🏗️_Continuous_Beam_Analysis.py")

with col2:
    if st.button("🏠 กลับหน้าแรก"):
        st.switch_page("home.py")

with col3:
    if st.button("🌉 Bridge Analysis"):
        st.switch_page("pages/3_🌉_Bridge_Analysis.py")
