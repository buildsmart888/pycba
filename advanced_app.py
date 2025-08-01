import streamlit as st
import numpy as np
import pandas as pd
from pycba.beam import Beam
from pycba.analysis import BeamAnalysis
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="Analysis of Continuous Beam", layout="wide")

def create_beam_diagram(span_lengths, wdl, wll, load_factors, moment_left, moment_right, reactions=None):
    """สร้างแผนภาพคานและน้ำหนักบรรทุก พร้อมแสดงแรงปฏิกิริยา
    load_factors: [load_factor_dl, load_factor_ll]
    """
    fig = go.Figure()
    
    # คำนวณความยาวรวม
    total_length = sum(span_lengths)
    y_base = 0
    
    # วาดเส้นคาน
    current_x = 0
    beam_x = [0]
    beam_y = [y_base]
    
    for span_length in span_lengths:
        current_x += span_length
        beam_x.append(current_x)
        beam_y.append(y_base)
    
    # เส้นคาน
    fig.add_trace(go.Scatter(
        x=beam_x, y=beam_y,
        mode='lines',
        line=dict(color='purple', width=8),
        showlegend=False
    ))
    
    # จุดรองรับและแรงปฏิกิริยา
    current_x = 0
    for i in range(len(span_lengths) + 1):
        # จุดรองรับ
        fig.add_trace(go.Scatter(
            x=[current_x], y=[y_base - 0.3],
            mode='markers',
            marker=dict(symbol='triangle-up', size=15, color='green'),
            showlegend=False
        ))
        
        # แสดงหมายเลขจุดรองรับ
        if i == 0:
            label = "0"
        elif i == len(span_lengths):
            label = "n"
        else:
            label = str(i)
        
        fig.add_trace(go.Scatter(
            x=[current_x], y=[y_base - 0.6],
            mode='text',
            text=[label],
            textfont=dict(size=12, color='blue'),
            showlegend=False
        ))
        
        # แสดงแรงปฏิกิริยาถ้ามี
        if reactions is not None and i < len(reactions):
            # แสดงลูกศรแรงปฏิกิริยา (ลูกศรขึ้น)
            fig.add_trace(go.Scatter(
                x=[current_x, current_x], y=[y_base - 0.3, y_base - 0.8],
                mode='lines',
                line=dict(color='red', width=3),
                showlegend=False
            ))
            # หัวลูกศร
            fig.add_trace(go.Scatter(
                x=[current_x], y=[y_base - 0.3],
                mode='text',
                text=["↑"],
                textfont=dict(color='red', size=16),
                showlegend=False
            ))
            # แสดงค่าแรงปฏิกิริยา
            fig.add_trace(go.Scatter(
                x=[current_x], y=[y_base - 1.0],
                mode='text',
                text=[f"R{i}={reactions[i]:.0f} kg"],
                textfont=dict(size=10, color='red'),
                showlegend=False
            ))
        
        if i < len(span_lengths):
            current_x += span_lengths[i]
    
    # น้ำหนักบรรทุก
    load_factor_dl, load_factor_ll = load_factors
    total_load = (wdl * load_factor_dl) + (wll * load_factor_ll)
    if total_load > 0:
        # วาดลูกศรแสดงน้ำหนักกระจาย
        arrow_count = 20
        for i, span_length in enumerate(span_lengths):
            span_start = sum(span_lengths[:i])
            arrow_spacing = span_length / arrow_count
            
            for j in range(arrow_count + 1):
                x = span_start + j * arrow_spacing
                if x <= span_start + span_length:
                    fig.add_trace(go.Scatter(
                        x=[x, x], y=[y_base + 0.8, y_base],
                        mode='lines',
                        line=dict(color='red', width=1),
                        showlegend=False
                    ))
                    # ลูกศร
                    fig.add_trace(go.Scatter(
                        x=[x], y=[y_base + 0.8],
                        mode='text',
                        text=["↓"],
                        textfont=dict(color='red', size=8),
                        showlegend=False
                    ))
    
    # แสดงค่าน้ำหนักบรรทุกเหนือแต่ละช่วง
    current_x = 0
    for i, span_length in enumerate(span_lengths):
        mid_x = current_x + span_length / 2
        
        # แสดงน้ำหนักบรรทุก
        if total_load > 0:
            fig.add_trace(go.Scatter(
                x=[mid_x], y=[y_base + 1.3],
                mode='text',
                text=[f"{total_load:.0f} kg/m"],
                textfont=dict(color='red', size=12),
                showlegend=False
            ))
        
        # แสดงความยาวช่วง
        fig.add_trace(go.Scatter(
            x=[mid_x], y=[y_base - 1.3],
            mode='text',
            text=[f"{span_length:.1f} m"],
            textfont=dict(size=12),
            showlegend=False
        ))
        
        current_x += span_length
    
    # โมเมนต์ลบ
    if moment_left != 0:
        # วาดลูกศรโค้งสำหรับโมเมนต์
        fig.add_trace(go.Scatter(
            x=[0], y=[y_base + 0.5],
            mode='text',
            text=[f"{moment_left:.0f} kg-m"],
            textfont=dict(color='red', size=12),
            showlegend=False
        ))
    
    if moment_right != 0:
        fig.add_trace(go.Scatter(
            x=[total_length], y=[y_base + 0.5],
            mode='text',
            text=[f"{moment_right:.0f} kg-m"],
            textfont=dict(color='red', size=12),
            showlegend=False
        ))
    
    # แสดงความยาวรวม
    fig.add_trace(go.Scatter(
        x=[total_length/2], y=[y_base - 1.8],
        mode='text',
        text=[f"{total_length} m"],
        textfont=dict(size=14, color='black'),
        showlegend=False
    ))
    
    # เส้นอ้างอิงความยาวรวม
    fig.add_trace(go.Scatter(
        x=[0, 0, total_length, total_length], 
        y=[y_base - 1.6, y_base - 1.7, y_base - 1.7, y_base - 1.6],
        mode='lines',
        line=dict(color='black', width=1),
        showlegend=False
    ))
    
    # ปรับแต่งกราฟ
    fig.update_layout(
        height=350,
        xaxis=dict(
            showgrid=False, 
            zeroline=False, 
            showticklabels=False,
            range=[0, total_length]  # กำหนดช่วง x-axis ให้ตรงกับความยาวคาน
        ),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white'
    )
    
    return fig

def create_shear_diagram(x_points, shear):
    """สร้างแผนภาพแรงเฉือน"""
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
        showlegend=False
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
        height=200,
        xaxis=dict(
            title="",
            showgrid=False,
            range=[0, total_length]  # กำหนดช่วง x-axis ให้ตรงกับ FBD
        ),
        yaxis_title="",
        margin=dict(l=50, r=20, t=20, b=50),
        plot_bgcolor='white'
    )
    
    return fig

def create_moment_diagram(x_points, moment):
    """สร้างแผนภาพโมเมนต์"""
    fig = go.Figure()
    
    # คำนวณความยาวรวมจาก x_points
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
        showlegend=False
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
            text=[f"{max_moment:.0f} kg-m"],
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
            text=[f"{min_moment:.0f} kg-m"],
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
        height=200,
        xaxis=dict(
            title="",
            showgrid=False,
            range=[0, total_length]  # กำหนดช่วง x-axis ให้ตรงกับ FBD
        ),
        yaxis_title="",
        margin=dict(l=50, r=20, t=20, b=50),
        plot_bgcolor='white'
    )
    
    return fig

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background-color: #003399;
        color: white;
        padding: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-header {
        background-color: #f0f0f0;
        padding: 8px;
        margin: 10px 0;
        border-left: 4px solid #003399;
        font-weight: bold;
    }
    .result-box {
        background-color: #e8f4f8;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-family: monospace;
    }
    .input-section {
        background-color: #f8f9fa;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #dee2e6;
        border-radius: 5px;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">Analysis of Continuous Beam</div>', unsafe_allow_html=True)

# Navigation links (cosmetic)
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
with col_nav1:
    st.markdown("**CONBEAM Home**")
with col_nav2:
    st.markdown("**About**")
with col_nav3:
    st.markdown("**Print**")
with col_nav4:
    st.markdown("**SKETCHUP&CIVIL_ENGINEER**")

# Main layout
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown('<div class="section-header">ช่วงคานและน้ำหนักบรรทุก:</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        
        # จำนวนช่วงคาน
        num_spans = st.number_input("จำนวนช่วง:", min_value=1, max_value=10, value=4, key="num_spans")
        
        # ความยาวแต่ละช่วง
        st.markdown("**ความยาวแต่ละช่วง (เมตร):**")
        span_lengths = []
        for i in range(num_spans):
            span_length = st.number_input(
                f"คานช่วงที่ {i+1} ยาว:", 
                min_value=0.1, 
                value=5.0, 
                step=0.1, 
                key=f"span_{i}"
            )
            span_lengths.append(span_length)
        
        # แสดงความยาวรวม
        total_length = sum(span_lengths)
        st.info(f"ความยาวรวม: {total_length:.1f} เมตร")
        
        # น้ำหนักบรรทุก
        wdl = st.number_input("น้ำหนักแผ่คงที่ WDL:", value=1200.0, step=10.0, key="wdl", help="Dead Load (kg/m)")
        wll = st.number_input("น้ำหนักบรรทุกจร WLL:", value=0.0, step=10.0, key="wll", help="Live Load (kg/m)")
        
        # Load Factor แยกกัน
        st.markdown("**Load Factors:**")
        load_factor_dl = st.number_input("Load Factor สำหรับ DL:", value=1.2, step=0.1, key="load_factor_dl")
        load_factor_ll = st.number_input("Load Factor สำหรับ LL:", value=1.6, step=0.1, key="load_factor_ll")
        
        # แสดงน้ำหนักหลังการคูณ load factor
        factored_dl = wdl * load_factor_dl
        factored_ll = wll * load_factor_ll
        total_factored_load = factored_dl + factored_ll
        
        st.info(f"DL หลังคูณ Factor: {factored_dl:.0f} kg/m")
        st.info(f"LL หลังคูณ Factor: {factored_ll:.0f} kg/m")
        st.info(f"Total Load: {total_factored_load:.0f} kg/m")
        
        # โมเมนต์ลบ
        moment_left = st.number_input("โมเมนต์ลบข้างซ้าย:", value=0.0, step=100.0, key="moment_left")
        moment_right = st.number_input("โมเมนต์ลบข้างขวา:", value=0.0, step=100.0, key="moment_right")
        
        # ปุ่มวิเคราะห์
        analyze_button = st.button("วิเคราะห์", type="primary", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # แสดงผลการวิเคราะห์
    if analyze_button:
        try:
            # เตรียมข้อมูลสำหรับการวิเคราะห์
            # คุณสมบัติวัสดุ (ค่าเริ่มต้น)
            E = 200e6  # kN/m² (เปลี่ยนเป็น Pa สำหรับการคำนวณ)
            I = 0.0001  # m⁴
            
            # กำหนดจุดรองรับ
            R = []
            for i in range(num_spans + 1):
                if i == 0 or i == num_spans:  # จุดปลาย
                    R.extend([-1, -1])  # Fixed support
                else:  # จุดกลาง
                    R.extend([-1, 0])   # Pinned support
            
            # เตรียม Load Matrix
            LM = []
            
            # แปลงหน่วยจาก kg/m เป็น kN/m สำหรับน้ำหนักที่ผ่านการคูณ load factor แล้ว
            total_load_kn = total_factored_load / 1000  # แปลง kg เป็น kN
            
            # เพิ่มน้ำหนักแผ่กระจายในแต่ละช่วง
            for i in range(num_spans):
                if total_load_kn > 0:
                    LM.append([i+1, 1, -total_load_kn, 0.0, 0.0])  # UDL
            
            # เพิ่มโมเมนต์ลบถ้ามี (แปลงจาก kg-m เป็น kN-m)
            if moment_left != 0:
                moment_left_kn = moment_left / 1000  # ไม่ต้องคูณ load factor เพราะเป็นโมเมนต์ที่กำหนดไว้แล้ว
                LM.append([1, 4, -moment_left_kn, 0.0, 0.0])  # Moment at left end
            
            if moment_right != 0:
                moment_right_kn = moment_right / 1000  # ไม่ต้องคูณ load factor เพราะเป็นโมเมนต์ที่กำหนดไว้แล้ว
                LM.append([num_spans, 4, moment_right_kn, 1.0, 0.0])  # Moment at right end
            
            # สร้างและวิเคราะห์คาน
            analysis = BeamAnalysis(span_lengths, E*I, R, LM)
            analysis.analyze()
            
            # ดึงผลลัพธ์
            results = analysis.beam_results.results
            x_points = np.array(results.x)
            shear_kn = np.array(results.V)
            moment_kn = np.array(results.M)
            deflection = np.array(results.D) * 1000  # mm
            
            # แปลงกลับเป็น kg และ kg-m สำหรับการแสดงผล
            shear = shear_kn * 1000  # kN -> kg
            moment = moment_kn * 1000  # kN-m -> kg-m
            
            # คำนวณแรงปฏิกิริยาที่จุดรองรับ
            reactions = []
            current_x = 0
            
            for i in range(num_spans + 1):
                # หาแรงเฉือนที่ตำแหน่งจุดรองรับ
                idx = np.argmin(np.abs(x_points - current_x))
                
                if i == 0:
                    # จุดรองรับแรก - ใช้แรงเฉือนทางขวาของจุดนั้น (เป็นค่าบวก)
                    if idx + 1 < len(shear):
                        reaction = abs(shear[idx + 1])  # แรงเฉือนทางขวาของจุดรองรับ
                    else:
                        reaction = abs(shear[idx])
                elif i == num_spans:
                    # จุดรองรับสุดท้าย - ใช้แรงเฉือนทางซ้ายของจุดนั้น (เป็นค่าลบ)
                    if idx > 0:
                        reaction = abs(shear[idx - 1])  # แรงเฉือนทางซ้ายของจุดรองรับ
                    else:
                        reaction = abs(shear[idx])
                else:
                    # จุดรองรับกลาง - แรงปฏิกิริยา = แรงเฉือนซ้าย - แรงเฉือนขวา
                    shear_left = shear[idx] if idx > 0 else shear[idx]
                    shear_right = shear[idx + 1] if idx + 1 < len(shear) else shear[idx]
                    reaction = abs(shear_left - shear_right)
                
                reactions.append(reaction)
                
                if i < num_spans:
                    current_x += span_lengths[i]
            
            # แสดงแรงปฏิกิริยาที่จุดรองรับ
            st.markdown('<div class="section-header">แรงปฏิกิริยาที่จุดรองรับ:</div>', unsafe_allow_html=True)
            
            # แสดงผลแรงปฏิกิริยาที่จุดรองรับ
            reaction_text = ""
            for i, r in enumerate(reactions):
                reaction_text += f"R{i} = {r:.0f} kg<br>"
            
            st.markdown(f'<div class="result-box">{reaction_text}</div>', unsafe_allow_html=True)
            
            # สร้างแผนภาพ
            # 1. แผนภาพคาน (FBD)
            fig_beam = create_beam_diagram(span_lengths, wdl, wll, [load_factor_dl, load_factor_ll], moment_left, moment_right, reactions)
            st.markdown('<div class="section-header">FBD</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_beam, use_container_width=True)
            
            # 2. แผนภาพแรงเฉือน (SFD)
            fig_shear = create_shear_diagram(x_points, shear)
            st.markdown('<div class="section-header">SFD</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_shear, use_container_width=True)
            
            # 3. แผนภาพโมเมนต์ (BMD)
            fig_moment = create_moment_diagram(x_points, moment)
            st.markdown('<div class="section-header">BMD</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_moment, use_container_width=True)
            
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {str(e)}")
            st.error("กรุณาตรวจสอบข้อมูลนำเข้าและลองใหม่อีกครั้ง")

# Footer
st.markdown("---")
st.markdown("● SKETCHUP&CIVIL_ENGINEER")