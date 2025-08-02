import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    """Main home page for PyCBA Suite"""
    
    # Page configuration
    st.set_page_config(
        page_title="PyCBA Engineering Suite - Home",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2a5298;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .program-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .program-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .status-available {
        color: #28a745;
        font-weight: bold;
    }
    .status-coming {
        color: #ffc107;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-top: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ PyCBA Engineering Suite</h1>
        <h3>ชุดโปรแกรมวิศวกรรมโครงสร้าง สำหรับการวิเคราะห์และออกแบบ</h3>
        <p>Professional Structural Analysis Tools for Engineers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## 📋 เมนูหลัก")
        st.markdown("---")
        
        page = st.selectbox(
            "เลือกหน้าที่ต้องการ:",
            [
                "🏠 หน้าแรก",
                "📊 โปรแกรมทั้งหมด", 
                "🔧 เครื่องมือพิเศษ",
                "📚 คู่มือการใช้งาน",
                "👨‍💻 เกี่ยวกับเรา"
            ]
        )
        
        st.markdown("---")
        st.markdown("### 🔗 ลิงก์ด่วน")
        if st.button("🚀 เริ่มใช้งาน Beam Analysis"):
            st.switch_page("pages/1_🏗️_Continuous_Beam_Analysis.py")
    
    # Main Content based on selection
    if page == "🏠 หน้าแรก":
        show_home_page()
    elif page == "📊 โปรแกรมทั้งหมด":
        show_programs_page()
    elif page == "🔧 เครื่องมือพิเศษ":
        show_tools_page()
    elif page == "📚 คู่มือการใช้งาน":
        show_manual_page()
    elif page == "👨‍💻 เกี่ยวกับเรา":
        show_about_page()

def show_home_page():
    """Display home page content"""
    
    # Welcome Section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2 style="text-align: center; color: #2a5298;">🎯 ยินดีต้อนรับสู่ PyCBA Suite</h2>
            <p style="text-align: center; font-size: 1.1em;">
                ชุดโปรแกรมวิศวกรรมโครงสร้างที่ครบครันสำหรับวิศวกรและนักศึกษา<br>
                พัฒนาด้วย Python และ Streamlit เพื่อความแม่นยำและใช้งานง่าย
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Features
    st.markdown("## ✨ จุดเด่นของระบบ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔬 ความแม่นยำสูง</h3>
            <ul>
                <li>คำนวณตาม Matrix Method</li>
                <li>ผ่านการทดสอบ 23 test cases</li>
                <li>Success rate 100%</li>
                <li>เหมาะสำหรับงานวิชาการ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎨 UI/UX ที่ทันสมัย</h3>
            <ul>
                <li>กราฟแบบ Interactive</li>
                <li>Responsive Design</li>
                <li>รองรับทุกอุปกรณ์</li>
                <li>ใช้งานง่ายสำหรับทุกระดับ</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🌐 Online & Open Source</h3>
            <ul>
                <li>ใช้งานผ่าน Web Browser</li>
                <li>ไม่ต้องติดตั้งโปรแกรม</li>
                <li>รองรับ Multi-platform</li>
                <li>Source code เปิดให้ศึกษา</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("## 📈 สถิติการใช้งาน")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="โปรแกรมทั้งหมด",
            value="4",
            delta="1 ใหม่"
        )
    
    with col2:
        st.metric(
            label="Test Cases",
            value="23",
            delta="100% Pass"
        )
    
    with col3:
        st.metric(
            label="Performance",
            value="< 1s",
            delta="Very Fast"
        )
    
    with col4:
        st.metric(
            label="Platform Support",
            value="All",
            delta="Web-based"
        )

def show_programs_page():
    """Display all available programs"""
    
    st.markdown("## 📊 โปรแกรมทั้งหมดใน PyCBA Suite")
    
    # Create program data
    programs = [
        {
            "name": "🏗️ Continuous Beam Analysis",
            "description": "วิเคราะห์คานต่อเนื่องหลายช่วง พร้อมแสดงผล FBD, SFD, BMD",
            "features": [
                "วิเคราะห์คานต่อเนื่องได้หลายช่วง",
                "คำนวณแรงปฏิกิริยา (Reactions)",
                "แสดงแผนภาพ Free Body Diagram",
                "กราฟ Shear Force และ Bending Moment",
                "ปรับค่า Load Factor ได้"
            ],
            "status": "✅ พร้อมใช้งาน",
            "version": "v2.1",
            "url": "https://continuousbeamanalysis.streamlit.app/",
            "local_url": "pages/1_🏗️_Continuous_Beam_Analysis.py"
        },
        {
            "name": "🏗️ Beam Design - Strength Design Method",
            "description": "โปรแกรมออกแบบคานคอนกรีตเสริมเหล็ก ตามหลักการ Strength Design Method",
            "features": [
                "ออกแบบคานคอนกรีตเสริมเหล็ก",
                "คำนวณตาม Strength Design Method",
                "ตรวจสอบ Moment Capacity",
                "คำนวณ Steel Reinforcement",
                "ตรวจสอบ Shear และ Deflection"
            ],
            "status": "✅ พร้อมใช้งาน",
            "version": "v1.5",
            "url": "https://beam-design-sdm-app.streamlit.app/",
            "local_url": "pages/2_🏗️_Beam_Design_SDM.py"
        },
        {
            "name": "🌉 Bridge Analysis",
            "description": "วิเคราะห์สะพานและโครงสร้างขนาดใหญ่",
            "features": [
                "วิเคราะห์สะพานคอนกรีต",
                "คำนวณ Live Load Distribution",
                "ตรวจสอบตาม มาตรฐาน DPT",
                "Influence Lines Analysis",
                "Moving Load Analysis"
            ],
            "status": "🚧 กำลังพัฒนา",
            "version": "v1.0 (Beta)",
            "url": "#"
        },
        {
            "name": "🏢 Frame Analysis",
            "description": "วิเคราะห์โครงข้อแข็งสำหรับอาคาร",
            "features": [
                "วิเคราะห์โครงสร้างอาคาร 2D/3D",
                "คำนวณ Lateral Load",
                "ตรวจสอบ P-Delta Effect",
                "Seismic Analysis",
                "Wind Load Analysis"
            ],
            "status": "📅 วางแผนพัฒนา",
            "version": "Coming Soon",
            "url": "#",
            "local_url": "pages/4_🏢_Frame_Analysis.py"
        },
        {
            "name": "🔧 Section Properties",
            "description": "คำนวณคุณสมบัติหน้าตัดต่างๆ",
            "features": [
                "คำนวณ Area, Moment of Inertia",
                "Section Modulus",
                "Radius of Gyration",
                "Custom Shape Design",
                "Standard Steel Sections"
            ],
            "status": "📅 วางแผนพัฒนา",
            "version": "Coming Soon",
            "url": "#"
        }
    ]
    
    # Display programs
    for i, program in enumerate(programs):
        st.markdown(f"""
        <div class="program-card">
            <h3>{program['name']}</h3>
            <p><strong>เวอร์ชัน:</strong> {program['version']} | <span class="{'status-available' if '✅' in program['status'] else 'status-coming'}">{program['status']}</span></p>
            <p>{program['description']}</p>
            <details>
                <summary><strong>คุณสมบัติเด่น</strong></summary>
                <ul>
        """, unsafe_allow_html=True)
        
        for feature in program['features']:
            st.markdown(f"<li>{feature}</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></details></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col3:
            if "✅" in program['status']:
                if program.get('url') and program['url'] != "#":
                    # Check if it's external URL
                    if program['url'].startswith('http'):
                        if st.button(f"🌐 เปิดเว็บแอป", key=f"btn_{i}"):
                            st.markdown(f"� [เปิดในแท็บใหม่]({program['url']})")
                            st.info(f"คลิกลิงก์ด้านบนเพื่อเปิด {program['name']}")
                    else:
                        # Local page
                        if st.button(f"�🚀 เริ่มใช้งาน", key=f"btn_{i}"):
                            st.switch_page(program.get('local_url', program['url']))
            elif program['url'] == "#":
                if program.get('local_url'):
                    if st.button(f"📋 ดูรายละเอียด", key=f"btn_detail_{i}"):
                        st.switch_page(program['local_url'])
                else:
                    st.button("🔒 ยังไม่พร้อม", disabled=True, key=f"btn_disabled_{i}")

def show_tools_page():
    """Display special tools"""
    
    st.markdown("## 🔧 เครื่องมือพิเศษ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📐 Unit Converter</h3>
            <p>แปลงหน่วยต่างๆ สำหรับงานวิศวกรรม</p>
            <ul>
                <li>แรง (N, kN, kg, ton)</li>
                <li>ความยาว (m, cm, mm, in, ft)</li>
                <li>ความเค้น (Pa, MPa, GPa, psi)</li>
                <li>โมเมนต์ (N⋅m, kN⋅m, kg⋅m)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Load Calculator</h3>
            <p>คำนวณน้ำหนักบรรทุกตามมาตรฐาน</p>
            <ul>
                <li>Dead Load Calculator</li>
                <li>Live Load ตาม DPT 1008</li>
                <li>Wind Load ตาม DPT 1311</li>
                <li>Seismic Load ตาม DPT 1302</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("🚧 เครื่องมือเหล่านี้กำลังอยู่ในขั้นตอนการพัฒนา จะเปิดให้ใช้งานในเร็วๆ นี้")

def show_manual_page():
    """Display user manual"""
    
    st.markdown("## 📚 คู่มือการใช้งาน")
    
    # Manual sections
    manual_sections = {
        "🚀 เริ่มต้นใช้งาน": {
            "content": """
            ### ขั้นตอนการใช้งานครั้งแรก
            1. เลือกโปรแกรมที่ต้องการจากเมนูด้านซ้าย
            2. กรอกข้อมูลที่จำเป็น (ความยาวช่วง, โหลด)
            3. ปรับค่า Load Factor ตามความต้องการ
            4. กดปุ่ม "คำนวณ" เพื่อดูผลลัพธ์
            5. ดาวน์โหลดผลลัพธ์เป็นไฟล์ PDF หรือ Excel
            """,
            "image": None
        },
        "🏗️ Continuous Beam Analysis": {
            "content": """
            ### การใช้งาน Continuous Beam Analysis
            **ขั้นตอนที่ 1:** กำหนดจำนวนช่วงและความยาว
            - กรอกจำนวนช่วงที่ต้องการ (1-10 ช่วง)
            - ระบุความยาวแต่ละช่วงเป็นเมตร
            
            **ขั้นตอนที่ 2:** กำหนดโหลด
            - Dead Load (kg/m): น้ำหนักบรรทุกถาวร
            - Live Load (kg/m): น้ำหนักบรรทุกใช้สอย
            
            **ขั้นตอนที่ 3:** ปรับ Load Factor
            - Load Factor DL: ปกติใช้ 1.2
            - Load Factor LL: ปกติใช้ 1.6
            
            **ขั้นตอนที่ 4:** ดูผลลัพธ์
            - Free Body Diagram
            - Shear Force Diagram
            - Bending Moment Diagram
            - ค่าแรงปฏิกิริยา
            """,
            "image": None
        },
        "📋 ตัวอย่างการใช้งาน": {
            "content": """
            ### ตัวอย่าง: คานต่อเนื่อง 3 ช่วง
            
            **โจทย์:**
            - คานต่อเนื่อง 3 ช่วง ช่วงละ 6 เมตร
            - Dead Load = 1200 kg/m
            - Live Load = 800 kg/m
            
            **วิธีทำ:**
            1. เลือก "3 ช่วง" ในช่อง Number of Spans
            2. กรอกความยาว: 6, 6, 6 เมตร
            3. กรอก Dead Load: 1200 kg/m
            4. กรอก Live Load: 800 kg/m
            5. ใช้ Load Factor มาตรฐาน: DL=1.2, LL=1.6
            6. กดปุ่ม "คำนวณ"
            
            **ผลลัพธ์ที่ได้:**
            - แรงปฏิกิริยาที่จุดรองรับ
            - แผนภาพแรงเฉือนและโมเมนต์
            - ค่าโมเมนต์สูงสุดและตำแหน่ง
            """,
            "image": None
        }
    }
    
    # Display manual sections
    selected_section = st.selectbox(
        "เลือกหัวข้อที่ต้องการอ่าน:",
        list(manual_sections.keys())
    )
    
    if selected_section:
        section = manual_sections[selected_section]
        st.markdown(section["content"])
        
        if section.get("image"):
            st.image(section["image"], caption=f"ภาพประกอบ {selected_section}")
    
    # FAQ Section
    st.markdown("---")
    st.markdown("### ❓ คำถามที่พบบ่อย (FAQ)")
    
    with st.expander("Q: โปรแกรมนี้แม่นยำมากแค่ไหน?"):
        st.write("""
        A: โปรแกรมใช้วิธี Matrix Method ซึ่งเป็นวิธีมาตรฐานในการวิเคราะห์โครงสร้าง 
        ผ่านการทดสอบ 23 test cases ด้วย success rate 100% เหมาะสำหรับงานวิชาการและการใช้งานจริง
        """)
    
    with st.expander("Q: สามารถใช้งานบนมือถือได้หรือไม่?"):
        st.write("""
        A: ได้ครับ โปรแกรมออกแบบแบบ Responsive รองรับการใช้งานบนทุกอุปกรณ์ 
        ทั้งคอมพิวเตอร์ แท็บเล็ต และมือถือ
        """)
    
    with st.expander("Q: มีข้อจำกัดในการใช้งานหรือไม่?"):
        st.write("""
        A: ปัจจุบันรองรับ:
        - คานต่อเนื่องสูงสุด 10 ช่วง
        - โหลดแบบกระจายสม่ำเสมอ (UDL)
        - การรองรับแบบ Pin และ Fixed
        
        ฟีเจอร์เพิ่มเติมจะมีในเวอร์ชันต่อไป
        """)

def show_about_page():
    """Display about page"""
    
    st.markdown("## 👨‍💻 เกี่ยวกับเรา")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/300x200/2a5298/white?text=PyCBA+Logo", 
                caption="PyCBA Engineering Suite")
    
    with col2:
        st.markdown("""
        ### 🎯 วิสัยทัศน์
        พัฒนาเครื่องมือวิศวกรรมโครงสร้างที่ทันสมัย แม่นยำ และเข้าถึงได้ง่าย 
        เพื่อช่วยให้วิศวกรและนักศึกษาไทยมีเครื่องมือที่ดีในการทำงาน
        
        ### 🚀 พันธกิจ
        - สร้างโปรแกรมวิเคราะห์โครงสร้างที่แม่นยำ
        - ให้บริการฟรีสำหรับการศึกษา
        - พัฒนา Open Source Community
        - ส่งเสริมการใช้เทคโนโลยีในงานวิศวกรรม
        """)
    
    st.markdown("---")
    
    # Technical Details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🛠️ เทคโนโลยีที่ใช้
        - **Frontend**: Streamlit, Plotly
        - **Backend**: Python, NumPy, SciPy
        - **Analysis Engine**: PyCBA Library
        - **Testing**: Python unittest (23 test cases)
        - **Deployment**: Docker, Google Cloud
        """)
    
    with col2:
        st.markdown("""
        ### 📈 การพัฒนา
        - **เวอร์ชันปัจจุบัน**: v2.1
        - **เริ่มพัฒนา**: มกราคม 2025
        - **อัปเดตล่าสุด**: สิงหาคม 2025
        - **จำนวน Commits**: 150+
        - **Contributors**: 3 คน
        """)
    
    # Team Section
    st.markdown("### 👥 ทีมพัฒนา")
    
    team_members = [
        {
            "name": "Lead Developer",
            "role": "Full-Stack Development",
            "skills": "Python, Streamlit, Structural Analysis"
        },
        {
            "name": "Structural Engineer",
            "role": "Technical Validation",
            "skills": "Structural Design, Code Verification"
        },
        {
            "name": "UI/UX Designer",
            "role": "User Experience",
            "skills": "Interface Design, User Testing"
        }
    ]
    
    cols = st.columns(len(team_members))
    
    for i, member in enumerate(team_members):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <h4>{member['name']}</h4>
                <p><strong>{member['role']}</strong></p>
                <p><small>{member['skills']}</small></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Contact & Support
    st.markdown("---")
    st.markdown("### 📞 ติดต่อและสนับสนุน")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📧 Email Support**
        - support@pycba.com
        - technical@pycba.com
        """)
    
    with col2:
        st.markdown("""
        **🔗 Social Media**
        - GitHub: buildsmart888/pycba
        - LinkedIn: PyCBA Suite
        """)
    
    with col3:
        st.markdown("""
        **📚 Documentation**
        - User Manual
        - API Reference
        - Video Tutorials
        """)

def show_footer():
    """Display footer"""
    st.markdown("""
    <div class="footer">
        <p>© 2025 PyCBA Engineering Suite | Made with ❤️ in Thailand</p>
        <p>Open Source Project | Licensed under MIT</p>
        <p>Version 2.1 | Last Updated: August 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()
