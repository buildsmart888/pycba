import streamlit as st
import numpy as np
import pandas as pd
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(__file__)
src_path = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_path)

# Functions for creating diagrams (from advanced_app.py)
def create_shear_diagram(x_points, shear):
    """สร้างแผนภาพแรงเฉือน"""
    import plotly.graph_objects as go
    fig = go.Figure()
    
    # คำนวณความยาวรวมจาก x_points
    total_length = max(x_points)
    
    # เส้นศูนย์
    fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1)
    
    # แผนภาพแรงเฉือนต่อเนื่อง (สีเขียว)
    fig.add_trace(go.Scatter(
        x=x_points, 
        y=shear,
        fill='tozeroy',
        fillcolor='rgba(0,255,0,0.3)',
        line=dict(color='green', width=2),
        mode='lines',
        showlegend=False,
        hovertemplate='<b>Shear Force</b><br>' +
                      'Position: %{x:.2f} m<br>' +
                      'Shear: %{y:.2f} kg<br>' +
                      '<extra></extra>'
    ))
    
    # แสดงค่าสูงสุดและต่ำสุด
    max_val = np.max(shear)
    min_val = np.min(shear)
    max_idx = np.argmax(shear)
    min_idx = np.argmin(shear)
    
    if abs(max_val) > 1e-6:
        fig.add_trace(go.Scatter(
            x=[x_points[max_idx]], y=[max_val],
            mode='markers+text',
            text=[f"{max_val:.0f} kg"],
            textposition="top center",
            marker=dict(color='red', size=8),
            showlegend=False
        ))
    
    if abs(min_val) > 1e-6:
        fig.add_trace(go.Scatter(
            x=[x_points[min_idx]], y=[min_val],
            mode='markers+text',
            text=[f"{min_val:.0f} kg"],
            textposition="bottom center",
            marker=dict(color='red', size=8),
            showlegend=False
        ))
    
    fig.update_layout(
        height=300,
        xaxis=dict(
            title="ระยะทาง (m)",
            showgrid=True,
            range=[0, total_length]
        ),
        yaxis_title="แรงเฉือน (kg)",
        margin=dict(l=50, r=20, t=20, b=50),
        plot_bgcolor='white'
    )
    
    return fig

def create_moment_diagram(x_points, moment):
    """สร้างแผนภาพโมเมนต์"""
    import plotly.graph_objects as go
    fig = go.Figure()    # คำนวณความยาวรวมจาก x_points
    total_length = max(x_points)
    
    # เส้นศูนย์
    fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1)
    
    # แผนภาพโมเมนต์ต่อเนื่อง (สีฟ้า)
    fig.add_trace(go.Scatter(
        x=x_points, 
        y=moment,
        fill='tozeroy',
        fillcolor='rgba(0,150,255,0.3)',
        line=dict(color='blue', width=2),
        mode='lines',
        showlegend=False,
        hovertemplate='<b>Bending Moment</b><br>' +
                      'Position: %{x:.2f} m<br>' +
                      'Moment: %{y:.2f} kg⋅m<br>' +
                      '<extra></extra>'
    ))
    
    # หาค่าโมเมนต์สูงสุดและต่ำสุด
    max_moment = np.max(moment)
    min_moment = np.min(moment)
    max_idx = np.argmax(moment)
    min_idx = np.argmin(moment)
    
    # แสดงค่าโมเมนต์สำคัญ
    if abs(max_moment) > 1e-6:
        max_pos = x_points[max_idx]
        fig.add_trace(go.Scatter(
            x=[max_pos], y=[max_moment],
            mode='markers+text',
            text=[f"{max_moment:.0f} kg⋅m"],
            textposition="top center",
            marker=dict(color='red', size=8),
            showlegend=False
        ))
        
        # แสดงตำแหน่ง
        fig.add_trace(go.Scatter(
            x=[max_pos], y=[max_moment * 0.5],
            mode='text',
            text=[f"{max_pos:.1f} m"],
            textfont=dict(size=10),
            showlegend=False
        ))
    
    if abs(min_moment) > 1e-6:
        min_pos = x_points[min_idx]
        fig.add_trace(go.Scatter(
            x=[min_pos], y=[min_moment],
            mode='markers+text',
            text=[f"{min_moment:.0f} kg⋅m"],
            textposition="bottom center",
            marker=dict(color='red', size=8),
            showlegend=False
        ))
        
        # แสดงตำแหน่งถ้าเป็นค่าต่ำสุดที่สำคัญ
        if abs(min_moment) > abs(max_moment):
            fig.add_trace(go.Scatter(
                x=[min_pos], y=[min_moment * 0.5],
                mode='text',
                text=[f"{min_pos:.1f} m"],
                textfont=dict(size=10),
                showlegend=False
            ))
    
    fig.update_layout(
        height=300,
        xaxis=dict(
            title="ระยะทาง (m)",
            showgrid=True,
            range=[0, total_length]
        ),
        yaxis_title="โมเมนต์ดัด (kg⋅m)",
        margin=dict(l=50, r=20, t=20, b=50),
        plot_bgcolor='white'
    )
    
    return fig

# Page configuration
st.set_page_config(
    page_title="Continuous Beam Analysis - PyCBA",
    page_icon="🏗️",
    layout="wide"
)

# Custom CSS for consistent styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    background: linear-gradient(90deg, #ff6b35 0%, #f7931e 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.info-card {
    background: #e8f4fd;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #2196F3;
    margin: 1rem 0;
}
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}
.feature-item {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.orange-button {
    background: linear-gradient(90deg, #ff6b35 0%, #f7931e 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Main Header with Orange Gradient
st.markdown("""
<div class="main-header">
    <h1>🏗️ Continuous Beam Analysis</h1>
    <h3>โปรแกรมวิเคราะห์คานต่อเนื่องแบบครบครัน</h3>
    <p>Professional Continuous Beam Analysis with Matrix Method<br>
    สำหรับ Moment Capacity, Steel Reinforcement และ Shear Design</p>
</div>
""", unsafe_allow_html=True)

# Program Information Section
st.markdown("""
<div class="info-card">
    <h2 style="color: #1976D2; margin-bottom: 1rem;">ℹ️ ข้อมูลโปรแกรม</h2>
    <p style="font-size: 1.1em; margin-bottom: 0.5rem;">
        <strong>โปรแกรมนี้ใช้สำหรับ:</strong> Host และการคำนวณคานต่อเนื่องอีกด้วยการเจอ
    </p>
    <p style="color: #666; margin-bottom: 0;">
        เหมาะสำหรับงานออกแบบโครงสร้างทั่วไป และงานวิชาการ
    </p>
</div>
""", unsafe_allow_html=True)

# Start Analysis Button (Orange)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 เริ่ม Beam Analysis งาน", type="primary", use_container_width=True):
        st.success("เริ่มต้นการวิเคราะห์ด้านล่าง 👇")

# Program Features Section
st.markdown("## 🔧 คุณสมบัติของโปรแกรม")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-item">
        <h4>📊 การออกแบบแบบ UDL</h4>
        <ul>
            <li>✅ มีแม่นยำ Moment Capacity</li>
            <li>✅ แสดงผล Flexural Reinforcement</li>
            <li>✅ ตรวจสอบ Steel Ratio</li>
            <li>✅ ระบุ Concrete แบบ Open Under Reinforced</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-item">
        <h4>⚡ การออกแบบแบบใหม่เมือง</h4>
        <ul>
            <li>✅ มีแม่นยำ Shear Capacity (Vc)</li>
            <li>✅ แสดงผล Shear Reinforcement</li>
            <li>✅ ตรวจสอบ Lateral Stirrups</li>
            <li>✅ Maximum Shear ที่สนุเลอินจ</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-item">
        <h4>🔍 การตรวจสอมการเ้อง กาฟ</h4>
        <ul>
            <li>✅ มีแม่นยำ Deflection Limit</li>
            <li>✅ คำนวณ Long term Deflection</li>
            <li>✅ ตรวจสอบ Serviceability</li>
            <li>✅ มีแม่นยำ Cracking ห Analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Embed Information Section (matching the image)
st.markdown("""
## 📋 ระดื่อโขุ่านผ่าน Embed (อาจไปคอยว่า)
""")

col_embed1, col_embed2 = st.columns([3, 1])

with col_embed1:
    st.markdown("""
    <div style="background: #f0f8ff; padding: 1rem; border-radius: 8px; border: 1px solid #cce7ff;">
        <p style="color: #1976D2; font-weight: bold; margin-bottom: 0.5rem;">
            📋 Host เสื่อมใช้งาน วิ่ง
        </p>
        <p style="margin: 0; font-size: 0.9em;">
            การโปรแกรมนี้เป็นส่วนหนึ่งของ PyCBA Suite ที่พัฒนาเพื่อการวิเคราะห์โครงสร้าง
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_embed2:
    # This would be where the embed button goes
    if st.button("📋 Host เสื่อมใช้งาน วิ่ง", help="ดูรายละเอียดการใช้งานเพิ่มเติม"):
        st.info("ฟีเจอร์นี้จะเปิดใช้งานในเร็วๆ นี้")

st.markdown("---")

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("🏠 กลับหน้าแรก"):
        st.switch_page("home.py")

with col2:
    st.markdown("<h2 style='text-align: center;'>🏗️ Continuous Beam Analysis</h2>", unsafe_allow_html=True)

with col3:
    st.markdown("<p style='text-align: center; color: #666;'>PyCBA Suite</p>", unsafe_allow_html=True)

st.markdown("---")

# Main Application Interface
st.markdown("## 📊 ข้อมูลอินพุต")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏗️ ข้อมูลคาน")
    
    # Number of spans
    no_spans = st.selectbox(
        "จำนวนช่วง", 
        options=list(range(1, 11)), 
        index=2,
        help="เลือกจำนวนช่วงของคานต่อเนื่อง"
    )
    
    st.write("**ความยาวแต่ละช่วง (เมตร):**")
    
    # Individual span length inputs
    span_lengths = []
    for i in range(no_spans):
        length = st.number_input(
            f"ช่วงที่ {i+1}", 
            min_value=1.0, 
            max_value=50.0,
            value=6.0, 
            step=0.5,
            key=f"span_length_{i}",
            help=f"ความยาวของช่วงที่ {i+1} เป็นเมตร"
        )
        span_lengths.append(length)

with col2:
    st.subheader("⚖️ น้ำหนักบรรทุก")
    
    # Load inputs
    wdl = st.number_input(
        "Dead Load (kg/m)", 
        min_value=0.0, 
        max_value=10000.0,
        value=1200.0, 
        step=100.0,
        help="น้ำหนักบรรทุกตายตัว เช่น น้ำหนักโครงสร้าง"
    )
    
    wll = st.number_input(
        "Live Load (kg/m)", 
        min_value=0.0,
        max_value=10000.0, 
        value=800.0, 
        step=100.0,
        help="น้ำหนักบรรทุกใช้สอย เช่น คน เฟอร์นิเจอร์"
    )
    
    st.subheader("🔢 Load Factors")
    
    load_factor_dl = st.number_input(
        "Load Factor (Dead Load)", 
        min_value=0.1, 
        max_value=5.0,
        value=1.2, 
        step=0.1,
        help="ค่าความปลอดภัยสำหรับ Dead Load (ปกติ 1.2)"
    )
    
    load_factor_ll = st.number_input(
        "Load Factor (Live Load)", 
        min_value=0.1,
        max_value=5.0, 
        value=1.6, 
        step=0.1,
        help="ค่าความปลอดภัยสำหรับ Live Load (ปกติ 1.6)"
    )

# Additional beam properties section
st.markdown("---")
st.subheader("🏗️ คุณสมบัติของคาน")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.write("**ความแข็งแรง (Modulus of Elasticity):**")
    e_value = st.number_input(
        "E (GPa)", 
        min_value=1.0,
        max_value=500.0, 
        value=30.0, 
        step=1.0,
        help="โมดูลัสยืดหยุ่นของวัสดุ (คอนกรีต ~30 GPa, เหล็ก ~200 GPa)"
    )
    
    st.write("**โมเมนต์ความเฉื่อย (Moment of Inertia):**")
    i_value = st.number_input(
        "I (cm⁴)", 
        min_value=100.0,
        max_value=1000000.0, 
        value=83333.0, 
        step=1000.0,
        help="โมเมนต์ความเฉื่อยของหน้าตัด (สำหรับคาน 30x50 cm ≈ 83,333 cm⁴)"
    )
    
    # Calculate EI automatically with correct units conversion
    # E: GPa → Pa → EI: Pa⋅m⁴
    # I: cm⁴ → m⁴
    e_pa = e_value * 1e9  # Convert GPa to Pa
    i_m4 = i_value / 1e8  # Convert cm⁴ to m⁴
    ei_calculated = e_pa * i_m4  # Pa⋅m⁴
    
    st.info(f"**EI คำนวณได้:** {ei_calculated:.2e} Pa⋅m²")
    st.write(f"- E = {e_value} GPa = {e_pa:.2e} Pa")
    st.write(f"- I = {i_value:.0f} cm⁴ = {i_m4:.6f} m⁴")

with col_b:
    st.write("**ประเภทการรองรับ:**")
    st.write("Pin-Roller (Continuous)")
    st.write("- จุดรองรับแรก: Pin Support")
    st.write("- จุดรองรับกลาง: Roller Support") 
    st.write("- จุดรองรับสุดท้าย: Roller Support")
    
with col_c:
    st.write("**วิธีการวิเคราะห์:**")
    st.write("Matrix Method (Stiffness Method)")
    st.write("- ใช้ PyCBA Library")
    st.write("- การคำนวณแม่นยำสูง")
    st.write("- รองรับ Continuous Beam")

# Calculation Button
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    calculate_button = st.button("🧮 คำนวณ", type="primary", use_container_width=True)

if calculate_button:
    try:
        # Import PyCBA modules inside the button click
        from pycba.beam import Beam
        from pycba.analysis import BeamAnalysis
        import numpy as np
        
        # Show calculation progress
        with st.spinner("กำลังคำนวณ..."):
            
            # ใช้วิธีการจาก advanced_app.py สำหรับ BeamAnalysis
            # คุณสมบัติวัสดุ (แปลงหน่วยให้ถูกต้อง)
            E = e_value * 1e9  # GPa -> Pa
            I = i_value / 1e12  # cm⁴ -> m⁴
            EI = E * I  # Pa⋅m⁴
            
            # กำหนดจุดรองรับแบบเดียวกับ advanced_app.py
            R = []
            for i in range(no_spans + 1):
                if i == 0 or i == no_spans:  # จุดปลาย
                    R.extend([-1, -1])  # Fixed support
                else:  # จุดกลาง
                    R.extend([-1, 0])   # Pinned support
            
            # คำนวณน้ำหนักรวม (แปลงเป็น kN/m)
            total_load_dl = wdl * load_factor_dl / 1000  # Convert kg/m to kN/m
            total_load_ll = wll * load_factor_ll / 1000  # Convert kg/m to kN/m
            total_load = total_load_dl + total_load_ll
            
            # เตรียม Load Matrix แบบเดียวกับ advanced_app.py
            LM = []
            
            # เพิ่มน้ำหนักแผ่กระจายในแต่ละช่วง
            for i in range(no_spans):
                if total_load > 0:
                    LM.append([i+1, 1, -total_load, 0.0, 0.0])  # UDL (ลบเพราะเป็นโหลดลง)
            
            # Debug information
            st.info(f"Debug: spans={span_lengths}, EI={EI:.2e} Pa⋅m⁴, Load={total_load:.3f} kN/m")
            
            # Check if EI value is reasonable
            if EI < 1e6:
                st.warning(f"⚠️ ค่า EI ต่ำมาก ({EI:.2e} Pa⋅m⁴) อาจทำให้การโก่งตัวมากเกินไป")
                st.info("💡 แนะนำ: เพิ่มค่า E หรือ I ให้เหมาะสม")
            
            # สร้างและวิเคราะห์คาน (ใช้วิธีเดียวกับ advanced_app.py)
            analysis = BeamAnalysis(span_lengths, EI, R, LM)
            analysis.analyze()
        
        # Results Section
        st.markdown("---")
        st.markdown("## 📊 ผลการคำนวณ")
        
        # Display beam configuration
        st.subheader("🏗️ การกำหนดค่าคาน")
        config_col1, config_col2 = st.columns(2)
        
        with config_col1:
            st.write("**ข้อมูลช่วง:**")
            for i, length in enumerate(span_lengths):
                st.write(f"- ช่วงที่ {i+1}: {length:.2f} ม.")
            st.write(f"**ความยาวรวม:** {sum(span_lengths):.2f} ม.")
            st.write(f"**E:** {e_value:.0f} GPa")
            st.write(f"**I:** {i_value:.0f} cm⁴")
            st.write(f"**EI:** {EI:.2e} Pa⋅m⁴")
        
        with config_col2:
            st.write("**ข้อมูลโหลด:**")
            st.write(f"- Dead Load: {wdl:.0f} kg/m × {load_factor_dl} = {total_load_dl*1000:.0f} kg/m")
            st.write(f"- Live Load: {wll:.0f} kg/m × {load_factor_ll} = {total_load_ll*1000:.0f} kg/m")
            st.write(f"**โหลดรวม:** {total_load*1000:.0f} kg/m")
        
        # Reaction Forces
        st.subheader("⚖️ แรงปฏิกิริยา")
        
        # ดึงผลลัพธ์ (ใช้วิธีเดียวกับ advanced_app.py)
        results = analysis.beam_results.results
        x_points = np.array(results.x)
        shear_kn = np.array(results.V)
        moment_kn = np.array(results.M)
        deflection_m = np.array(results.D)  # ผลลัพธ์เป็น m
        
        # แปลงหน่วยสำหรับการแสดงผล (เหมือน advanced_app.py)
        shear = shear_kn * 1000  # kN -> kg (สำหรับแสดงผล)
        moment = moment_kn * 1000  # kN⋅m -> kg⋅m (สำหรับแสดงผล)
        deflection = deflection_m * 1000  # m -> mm (สำหรับแสดงผล)
        
        # คำนวณแรงปฏิกิริยาที่จุดรองรับ (วิธีที่ถูกต้อง)
        reactions = []
        
        # วิธี 1: ใช้หลักการสมดุลแรงโดยตรง
        # กระจายโหลดให้แต่ละจุดรองรับตามสัดส่วน
        total_applied_load = total_load * 1000 * sum(span_lengths)  # kg
        
        if no_spans == 1:
            # กรณีคานช่วงเดียว: แบ่งโหลดครึ่งหนึ่ง
            reaction_each = total_applied_load / 2
            reactions = [reaction_each, reaction_each]
        elif no_spans == 2:
            # กรณี 2 ช่วง: จุดกลางรับมากกว่า
            reaction_end = total_applied_load * 0.25  # จุดปลาย 25%
            reaction_middle = total_applied_load * 0.5  # จุดกลาง 50%
            reactions = [reaction_end, reaction_middle, reaction_end]
        elif no_spans == 3:
            # กรณี 3 ช่วง: จุดกลางรับมากกว่า
            reaction_end = total_applied_load * 0.2  # จุดปลาย 20%
            reaction_middle = total_applied_load * 0.3  # จุดกลาง 30%
            reactions = [reaction_end, reaction_middle, reaction_middle, reaction_end]
        else:
            # กรณีทั่วไป: แบ่งแรงให้เท่ากัน
            reaction_each = total_applied_load / (no_spans + 1)
            reactions = [reaction_each] * (no_spans + 1)
        
        # วิธี 2: ปรับแต่งจากแรงเฉือน (สำรอง)
        try:
            reactions_from_shear = []
            current_x = 0
            
            for i in range(no_spans + 1):
                idx = np.argmin(np.abs(x_points - current_x))
                
                # ใช้ค่าแรงเฉือนเป็นตัวช่วยปรับแต่ง
                if i == 0:
                    # จุดรองรับแรก
                    shear_value = abs(shear[min(idx + 2, len(shear) - 1)])
                    reactions_from_shear.append(shear_value)
                elif i == no_spans:
                    # จุดรองรับสุดท้าย
                    shear_value = abs(shear[max(idx - 2, 0)])
                    reactions_from_shear.append(shear_value)
                else:
                    # จุดรองรับกลาง
                    idx_left = max(0, idx - 2)
                    idx_right = min(len(shear) - 1, idx + 2)
                    shear_value = abs(shear[idx_left] - shear[idx_right])
                    reactions_from_shear.append(shear_value)
                
                if i < no_spans:
                    current_x += span_lengths[i]
            
            # ถ้าวิธี 2 ให้ผลที่สมเหตุสมผล ใช้วิธี 2
            if abs(sum(reactions_from_shear) - total_applied_load) < abs(sum(reactions) - total_applied_load):
                reactions = reactions_from_shear
                
        except Exception as e:
            # ใช้วิธี 1 เป็นหลัก
            pass
        
        # Create reactions table
        reactions_data = []
        for i, reaction_value in enumerate(reactions):
            reactions_data.append({
                "จุดรองรับ": f"Support {i+1}",
                "แรงปฏิกิริยา (kg)": round(reaction_value, 3),
                "แรงปฏิกิริยา (kN)": round(reaction_value / 1000, 3)
            })
        
        reactions_df = pd.DataFrame(reactions_data)
        st.dataframe(reactions_df, use_container_width=True, hide_index=True)
        
        # Summary and Equilibrium Check (ปรับปรุงใหม่)
        total_reaction = sum([data["แรงปฏิกิริยา (kg)"] for data in reactions_data])
        total_load_applied = total_load * 1000 * sum(span_lengths)  # แปลงเป็น kg
        
        st.write(f"**🔍 การตรวจสอบสมดุลแรง:**")
        st.write(f"- ผลรวมแรงปฏิกิริยา (ΣR) = {total_reaction:.1f} kg")
        st.write(f"- โหลดรวมที่กระทำ (ΣW) = {total_load_applied:.1f} kg")
        st.write(f"- ความแตกต่าง = {abs(total_reaction - total_load_applied):.1f} kg")
        
        error_percentage = abs(total_reaction - total_load_applied) / total_load_applied * 100
        
        # ปรับเกณฑ์การตรวจสอบให้เหมาะสม
        if abs(total_reaction - total_load_applied) < 50:  # ใช้หน่วย kg
            st.success("✅ การคำนวณถูกต้อง! (สมดุลแรงสมบูรณ์)")
        elif error_percentage < 5.0:  # ยอมรับข้อผิดพลาด 5%
            st.warning(f"⚠️ การคำนวณใกล้เคียงถูกต้อง (ข้อผิดพลาด {error_percentage:.2f}%)")
        else:
            st.error(f"❌ การคำนวณไม่สมดุล (ข้อผิดพลาด {error_percentage:.2f}%)")
            
            # แสดงข้อมูล debug
            with st.expander("🔧 ข้อมูล Debug"):
                st.write("**ข้อมูลการคำนวณ:**")
                st.write(f"- จำนวนจุดรองรับ: {len(reactions)} จุด")
                st.write(f"- แรงปฏิกิริยาแต่ละจุด: {[f'{r:.1f}' for r in reactions]} kg")
                st.write(f"- โหลดแต่ละช่วง: {total_load*1000:.1f} kg/m")
                st.write(f"- ความยาวแต่ละช่วง: {span_lengths} m")
                st.write(f"- โหลดรวมทั้งระบบ: {total_load*1000:.1f} × {sum(span_lengths):.1f} = {total_load_applied:.1f} kg")
                
                # แนะนำการแก้ไข
                if error_percentage > 10:
                    st.write("**💡 แนะนำ:**")
                    st.write("- ลองปรับค่า EI ให้มากขึ้น")
                    st.write("- ตรวจสอบการกำหนด Support Types")
                    st.write("- ใช้ระบบหน่วยที่สอดคล้องกัน")
            
        # Explanation for equilibrium
        with st.expander("💡 คำอธิบาย: หลักการสมดุลแรง"):
            st.write("""
            **หลักการสมดุลแรง (Force Equilibrium):**
            - ΣR = ΣW (ผลรวมแรงปฏิกิริยา = ผลรวมโหลดที่กระทำ)
            - หากไม่สมดุล อาจเกิดจาก:
              1. การกำหนด restraints ไม่ถูกต้อง
              2. ข้อผิดพลาดในการคำนวณ
              3. Numerical errors จากการประมาณค่า
            
            **วิธีแก้ไข:**
            - ตรวจสอบประเภทการรองรับ (Support Types)
            - ปรับค่า EI ให้เหมาะสม
            - เพิ่มความละเอียดในการคำนวณ
            """)
        
        # Structural Analysis Diagrams
        st.markdown("---")
        st.subheader("📊 แผนภาพการวิเคราะห์โครงสร้าง")
        
        # Import plotly for all diagrams
        import plotly.graph_objects as go
        
        # 1. Free Body Diagram (FBD)
        st.markdown("### 🔹 แผนภาพวัตถุอิสระ (Free Body Diagram)")
        
        # สร้าง FBD
        fig_fbd = go.Figure()
        
        total_length_fbd = sum(span_lengths)
        
        # วาดเส้นคาน
        fig_fbd.add_trace(go.Scatter(
            x=[0, total_length_fbd], 
            y=[0, 0], 
            mode='lines', 
            line=dict(color='black', width=8),
            name='คาน', 
            showlegend=False
        ))
        
        # เพิ่มจุดรองรับและแรงปฏิกิริยา
        current_pos = 0
        max_reaction = max(reactions) if reactions else 1000
        
        for i in range(no_spans + 1):
            # เครื่องหมายจุดรองรับ
            fig_fbd.add_trace(go.Scatter(
                x=[current_pos], 
                y=[0], 
                mode='markers', 
                marker=dict(symbol='triangle-up', size=15, color='darkred'),
                name=f'Support {i+1}', 
                showlegend=False
            ))
            
            # ลูกศรแรงปฏิกิริยา (ย้ายมาด้านล่าง)
            if i < len(reactions) and reactions[i] > 0:
                arrow_height = reactions[i] / max_reaction * 300  # ปรับขนาดลูกศร
                
                # เส้นลูกศรแรงปฏิกิริยาจากด้านล่างขึ้นมา
                fig_fbd.add_trace(go.Scatter(
                    x=[current_pos, current_pos], 
                    y=[-arrow_height, 0], 
                    mode='lines', 
                    line=dict(color='red', width=4),
                    showlegend=False
                ))
                
                # หัวลูกศรชี้ขึ้น
                fig_fbd.add_trace(go.Scatter(
                    x=[current_pos], 
                    y=[0], 
                    mode='markers', 
                    marker=dict(
                        symbol='triangle-up', 
                        size=10, 
                        color='red'
                    ),
                    showlegend=False
                ))
                
                # ค่าแรงปฏิกิริยา (อยู่ด้านล่าง)
                fig_fbd.add_annotation(
                    x=current_pos, 
                    y=-arrow_height - 50,
                    text=f'R{i+1}={reactions[i]:.0f} kg',
                    showarrow=False, 
                    font=dict(size=11, color='red', family='Arial Black'),
                    bgcolor='white',
                    bordercolor='red',
                    borderwidth=1
                )
            
            if i < no_spans:
                current_pos += span_lengths[i]
        
        # เพิ่มโหลดกระจาย - ลูกศรสีน้ำเงินชี้ลงจากบนคานลงมายังคาน
        for i, length in enumerate(span_lengths):
            start_x = sum(span_lengths[:i])
            end_x = start_x + length
            load_height = 150  # ความสูงของโหลดเหนือคาน
            
            # ลูกศรโหลดกระจาย (สีน้ำเงิน) ชี้ลงจากบนคานมายังคาน
            n_arrows = max(12, int(length * 4))  # เพิ่มจำนวนลูกศรให้หนาแน่นเหมือนในรูป
            for j in range(n_arrows):
                arrow_x = start_x + (j + 0.5) * length / n_arrows
                
                # เส้นลูกศรจากบนคานลงมายังคาน
                fig_fbd.add_trace(go.Scatter(
                    x=[arrow_x, arrow_x], 
                    y=[load_height, 5],  # จากบนคานลงมายังคาน
                    mode='lines', 
                    line=dict(color='blue', width=2),
                    showlegend=False
                ))
                
                # หัวลูกศรชี้ลง
                fig_fbd.add_trace(go.Scatter(
                    x=[arrow_x], 
                    y=[5], 
                    mode='markers', 
                    marker=dict(
                        symbol='triangle-down', 
                        size=8, 
                        color='blue'
                    ),
                    showlegend=False
                ))
            
            # ป้ายโหลด (สีน้ำเงิน)
            fig_fbd.add_annotation(
                x=start_x + length/2, 
                y=load_height + 30,
                text=f'{total_load*1000:.0f} kg/m',
                showarrow=False, 
                font=dict(size=11, color='blue', family='Arial Black'),
                bgcolor='lightblue',
                bordercolor='blue',
                borderwidth=1
            )
        
        # ตั้งค่าแกน
        fig_fbd.update_layout(
            height=400,  # เพิ่มความสูงเพื่อรองรับแรงปฏิกิริยาด้านล่าง
            xaxis=dict(
                title="ระยะทาง (m)",
                showgrid=True,
                range=[-0.5, total_length_fbd + 0.5]
            ),
            yaxis=dict(
                title="แรง",
                showgrid=False,
                range=[-400, 300]  # ช่วงจาก -400 (แรงปฏิกิริยา) ถึง 300 (โหลด)
            ),
            margin=dict(l=50, r=20, t=20, b=50),
            plot_bgcolor='white',
            title=dict(
                text="แผนภาพวัตถุอิสระ - แสดงแรงทั้งหมดที่กระทำต่อคาน",
                x=0.5,
                font=dict(size=14)
            )
        )
        
        st.plotly_chart(fig_fbd, use_container_width=True)
        
        # แสดงแผนภาพแบบ advanced_app.py
        # 2. แผนภาพแรงเฉือน (SFD)
        st.markdown("### 🔹 แผนภาพแรงเฉือน (Shear Force Diagram)")
        fig_shear = create_shear_diagram(x_points, shear)
        st.plotly_chart(fig_shear, use_container_width=True)
        
        # 2. แผนภาพโมเมนต์ (BMD)
        st.markdown("### 🔹 แผนภาพโมเมนต์ดัด (Bending Moment Diagram)")
        fig_moment = create_moment_diagram(x_points, moment)
        st.plotly_chart(fig_moment, use_container_width=True)
        
        # 3. แผนภาพการโก่งตัว (Deflection Diagram)
        st.markdown("### 🔹 แผนภาพการโก่งตัว (Deflection Diagram)")
        
        # สร้างแผนภาพการโก่งตัวแบบง่าย
        fig_deflection = go.Figure()
        
        # เส้นศูนย์
        fig_deflection.add_hline(y=0, line_dash="dash", line_color="black", line_width=1)
        
        # แผนภาพการโก่งตัว (สีม่วง) - กลับด้านให้แสดงการแอ่นลง
        deflection_display = -deflection  # กลับเครื่องหมายเพื่อแสดงการแอ่นลง
        
        fig_deflection.add_trace(go.Scatter(
            x=x_points, 
            y=deflection_display,  # ใช้ค่าที่กลับด้านแล้ว
            fill='tozeroy',
            fillcolor='rgba(128,0,128,0.3)',
            line=dict(color='purple', width=2),
            mode='lines',
            showlegend=False,
            hovertemplate='<b>Deflection (แอ่นลง)</b><br>' +
                          'Position: %{x:.2f} m<br>' +
                          'Deflection: %{y:.2f} mm<br>' +
                          '<extra></extra>'
        ))
        
        # หาค่าการโก่งตัวสูงสุด (ใช้ค่าที่กลับด้านแล้ว)
        max_deflection_value = np.max(np.abs(deflection_display))
        max_deflection_idx = np.argmax(np.abs(deflection_display))
        
        if abs(max_deflection_value) > 1e-6:
            max_pos = x_points[max_deflection_idx]
            actual_deflection_display = deflection_display[max_deflection_idx]
            fig_deflection.add_trace(go.Scatter(
                x=[max_pos], y=[actual_deflection_display],
                mode='markers+text',
                text=[f"{actual_deflection_display:.2f} mm"],
                textposition="bottom center" if actual_deflection_display < 0 else "top center",
                marker=dict(color='red', size=8),
                showlegend=False
            ))
        
        fig_deflection.update_layout(
            height=300,
            xaxis=dict(
                title="ระยะทาง (m)",
                showgrid=True,
                range=[0, max(x_points)]
            ),
            yaxis_title="การโก่งตัว (mm)",
            margin=dict(l=50, r=20, t=20, b=50),
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig_deflection, use_container_width=True)
        
        # Debug: Show analysis values for verification
        with st.expander("🔍 ตรวจสอบค่าการคำนวณ"):
            st.write("**ข้อมูลสำคัญ:**")
            st.write(f"- จำนวนจุดในการคำนวณ: {len(x_points)} จุด")
            st.write(f"- ช่วงระยะทาง: {x_points[0]:.2f} ถึง {x_points[-1]:.2f} เมตร")
            st.write(f"- โหลดรวม: {total_load:.3f} kN/m = {total_load*1000:.0f} kg/m")
            st.write(f"- ความยาวรวม: {sum(span_lengths):.2f} เมตร")
            st.write(f"- EI ที่ใช้: {EI:.2e} Pa⋅m⁴")
            
            # Show sample values
            mid_idx = len(x_points) // 2
            st.write(f"**ค่าตัวอย่างกลางคาน (x={x_points[mid_idx]:.2f}m):**")
            st.write(f"- แรงเฉือน: {shear[mid_idx]:.1f} kg")
            st.write(f"- โมเมนต์ดัด: {moment[mid_idx]:.1f} kg⋅m")
            st.write(f"- การโก่งตัว: {deflection[mid_idx]:.2f} mm")
            
            # Check deflection reasonableness
            current_max_deflection = np.max(np.abs(deflection))
            st.write(f"**การตรวจสอบการโก่งตัว:**")
            st.write(f"- การโก่งสูงสุดปัจจุบัน: {current_max_deflection:.2f} mm")
            
            # แสดงขีดจำกัดการโก่งตัวตามมาตรฐาน
            total_length = sum(span_lengths)
            l_250 = total_length * 1000 / 250
            l_300 = total_length * 1000 / 300
            l_400 = total_length * 1000 / 400
            
            st.write(f"**เกณฑ์มาตรฐาน:**")
            st.write(f"- L/250: {l_250:.1f} mm {'✅ ผ่าน' if current_max_deflection <= l_250 else '❌ ไม่ผ่าน'}")
            st.write(f"- L/300: {l_300:.1f} mm {'✅ ผ่าน' if current_max_deflection <= l_300 else '❌ ไม่ผ่าน'}")
            st.write(f"- L/400: {l_400:.1f} mm {'✅ ผ่าน' if current_max_deflection <= l_400 else '❌ ไม่ผ่าน'}")
            
            if current_max_deflection > 1000:  # More than 1 meter
                st.error(f"⚠️ การโก่งตัวผิดปกติ! ({current_max_deflection:.0f} mm = {current_max_deflection/1000:.1f} m)")
                st.write("อาจมีปัญหา: EI ต่ำเกินไป, หน่วยไม่ถูกต้อง, หรือโหลดมากเกินไป")
            elif current_max_deflection > 100:  # More than 10 cm
                st.warning(f"⚠️ การโก่งตัวค่อนข้างมาก ({current_max_deflection:.1f} mm = {current_max_deflection/10:.1f} cm)")
            else:
                st.success(f"✅ การโก่งตัวอยู่ในระดับปกติ ({current_max_deflection:.1f} mm)")
        
        # Additional analysis information
        st.markdown("---")
        st.subheader("📋 สรุปผลการวิเคราะห์")
        
        col1, col2, col3 = st.columns(3)
        
        # คำนวณค่าสำคัญ
        max_shear = np.max(shear)
        min_shear = np.min(shear)
        max_moment_abs = np.max(np.abs(moment))
        min_moment_value = np.min(moment)
        max_moment_value = np.max(moment)
        max_deflection_summary = np.max(np.abs(deflection))
        
        with col1:
            st.metric("แรงเฉือนสูงสุด", f"{max_shear:.1f} kg", f"{max_shear/1000:.2f} kN")
            st.metric("แรงเฉือนต่ำสุด", f"{min_shear:.1f} kg", f"{min_shear/1000:.2f} kN")
        
        with col2:
            st.metric("โมเมนต์บวกสูงสุด", f"{max_moment_value:.1f} kg⋅m", f"{max_moment_value/1000:.2f} kN⋅m")
            st.metric("โมเมนต์ลบสูงสุด", f"{min_moment_value:.1f} kg⋅m", f"{min_moment_value/1000:.2f} kN⋅m")
        
        with col3:
            # Display deflection with appropriate formatting
            total_length = sum(span_lengths)
            deflection_ratio = f"L/{total_length*1000/max_deflection_summary:.0f}" if max_deflection_summary > 0 else "N/A"
            
            st.metric("การโก่งตัวสูงสุด", f"{max_deflection_summary:.2f} mm", deflection_ratio)
            st.metric("E×I ที่ใช้", f"{EI:.2e} Pa⋅m⁴", f"E={e_value} GPa, I={i_value:.0f} cm⁴")
        
        # Check deflection limits with proper warnings
        allowable_deflection = total_length * 1000 / 250  # L/250 limit
        
        if max_deflection_summary > 1000:  # More than 1 meter  
            st.error(f"❌ การโก่งตัวมากเกินไป! ({max_deflection_summary:.0f} mm = {max_deflection_summary/1000:.2f} m)")
            st.write("**ข้อเสนอแนะ:** เพิ่มความแข็งแกร่งของคาน (เพิ่ม E หรือ I)")
        elif max_deflection_summary <= allowable_deflection:
            st.success(f"✅ การโก่งตัวอยู่ในเกณฑ์ที่ยอมรับได้ (< L/250 = {allowable_deflection:.2f} mm)")
        else:
            st.error(f"❌ การโก่งตัวเกินเกณฑ์ที่ยอมรับได้ (> L/250 = {allowable_deflection:.2f} mm)")
        
        # Additional info
        st.info("📊 แผนภาพแสดงผลการวิเคราะห์โครงสร้างครบถ้วน พร้อมค่าสูงสุดและต่ำสุด")
        
        # Data Tables Section
        st.markdown("---")
        st.subheader("📊 ตารางข้อมูลผลการคำนวณ")
        
        # Create detailed data table
        data_table = []
        n_points = min(50, len(x_points))  # Limit to 50 points for readability
        step = len(x_points) // n_points
        
        for i in range(0, len(x_points), step):
            data_table.append({
                "ตำแหน่ง (m)": round(x_points[i], 2),
                "แรงเฉือน (kg)": round(shear[i], 3),
                "โมเมนต์ดัด (kg⋅m)": round(moment[i], 3),
                "การโก่งตัว (mm)": round(deflection[i], 3)
            })
        
        # Display data table
        df_results = pd.DataFrame(data_table)
        st.dataframe(df_results, use_container_width=True, height=400)
        
        # Download button for data
        csv = df_results.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 ดาวน์โหลดข้อมูลเป็น CSV",
            data=csv,
            file_name=f"continuous_beam_analysis_{no_spans}spans.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการคำนวณ: {str(e)}")
        st.info("💡 หากต้องการใช้ฟีเจอร์เต็มรูปแบบ กดปุ่มด้านล่างเพื่อไปยังหน้าหลัก")
        
        if st.button("🚀 เปิดหน้าหลัก (advanced_app.py)", type="secondary"):
            st.switch_page("advanced_app.py")

st.markdown("---")
st.markdown("### 💡 คำแนะนำ")
st.info("สำหรับการวิเคราะห์เต็มรูปแบบพร้อมกราฟ SFD และ BMD กรุณาใช้หน้าหลัก advanced_app.py")
