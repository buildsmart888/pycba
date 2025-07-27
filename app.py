import streamlit as st
import numpy as np

from pycba.beam import Beam
from pycba.analysis import BeamAnalysis
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Continuous Beam Analysis", layout="wide")

st.title("โปรแกรมวิเคราะห์คานต่อเนื่อง")
st.write("วิเคราะห์คานต่อเนื่องไม่เกิน 5 ช่วง พร้อมแสดงผลแรงเฉือน โมเมนต์ดัด และการแอ่นตัว")

# Input section
with st.sidebar:
    st.header("ข้อมูลนำเข้า")
    
    # จำนวนช่วงคาน
    num_spans = st.number_input("จำนวนช่วงคาน", min_value=1, max_value=5, value=2)
    
    # คุณสมบัติวัสดุและหน้าตัด
    st.subheader("คุณสมบัติวัสดุและหน้าตัด")
    E = st.number_input("โมดูลัสยืดหยุ่น (E, kN/m²)", value=200e6, format="%e")
    I = st.number_input("โมเมนต์ความเฉื่อย (I, m⁴)", value=0.0001, format="%e")
    
    # Load factor
    load_factor = st.number_input("โหลดเฟคเตอร์", value=1.6, min_value=1.0)

# สร้าง columns สำหรับแต่ละช่วงคาน
spans_data = []
col1, col2 = st.columns(2)

with col1:
    st.subheader("ข้อมูลช่วงคาน")
    for i in range(num_spans):
        st.write(f"ช่วงคานที่ {i+1}")
        span_length = st.number_input(f"ความยาวช่วงคาน {i+1} (m)", value=5.0, key=f"span_{i}")
        udl = st.number_input(f"น้ำหนักแผ่กระจาย (kN/m) ช่วง {i+1}", value=0.0, key=f"udl_{i}")
        pl_value = st.number_input(f"น้ำหนักจุด (kN) ช่วง {i+1}", value=0.0, key=f"pl_{i}")
        pl_location = st.number_input(f"ตำแหน่งน้ำหนักจุด (m จากจุดเริ่มต้นช่วง) ช่วง {i+1}", 
                                    value=span_length/2, min_value=0.0, 
                                    max_value=span_length, key=f"pl_loc_{i}")
        spans_data.append({
            'length': span_length,
            'udl': udl,
            'pl': pl_value,
            'pl_location': pl_location
        })

# Calculate button
if st.button("วิเคราะห์คาน"):
    try:
        # รวบรวมข้อมูลคาน
        spans_lengths = [span['length'] for span in spans_data]
        
        # กำหนดจุดรองรับ
        # -1: จุดยึดแน่น (fixed)
        #  0: จุดหมุน (pinned)
        R = []
        for i in range(num_spans + 1):  # จำนวนจุดรองรับ = จำนวนช่วง + 1
            if i == 0:  # จุดแรก
                R.extend([-1, -1])  # กำหนดทั้งแรงและโมเมนต์
            elif i == num_spans:  # จุดสุดท้าย
                R.extend([-1, -1])  # กำหนดทั้งแรงและโมเมนต์
            else:  # จุดกลาง
                R.extend([-1, 0])  # กำหนดแรง แต่ปล่อยให้หมุนได้
        
        # เตรียมข้อมูลน้ำหนักบรรทุก
        LM = []  # Load Matrix
        
        # Debug: แสดงค่าที่จะใช้ในการคำนวณ
        st.write("### ตรวจสอบค่าที่ใช้ในการคำนวณ:")
        
        # ตรวจสอบและแก้ไข load matrix ตาม format ที่ถูกต้อง
        for i, span in enumerate(spans_data):
            st.write(f"ช่วงที่ {i+1}:")
            
            # ตรวจสอบ UDL (Type 1)
            if abs(span['udl']) > 1e-6:  # ใช้ค่าที่ใกล้เคียง 0 แทนการเทียบเท่ากับ 0
                udl_val = -span['udl']*load_factor  # เปลี่ยนเครื่องหมายเพื่อให้แรงกระทำลง
                st.write(f"- น้ำหนักแผ่กระจาย: {span['udl']} kN/m × {load_factor} = {udl_val} kN/m")
                # Format: [span_no, load_type=1(UDL), magnitude, a=0, c=0]
                LM.append([i+1, 1, udl_val, 0.0, 0.0])
            
            # ตรวจสอบ Point Load (Type 2)
            if abs(span['pl']) > 1e-6:
                pl_val = -span['pl']*load_factor  # เปลี่ยนเครื่องหมายเพื่อให้แรงกระทำลง
                relative_x = span['pl_location'] / span['length']
                st.write(f"- น้ำหนักจุด: {span['pl']} kN × {load_factor} = {pl_val} kN ที่ตำแหน่ง {relative_x:.3f}L")
                # Format: [span_no, load_type=2(PL), magnitude, a=relative_x, c=0]
                LM.append([i+1, 2, pl_val, relative_x, 0.0])
        
        st.write("### Load Matrix:")
        st.write(LM)
        
        # สร้างและวิเคราะห์คาน
        analysis = BeamAnalysis(spans_lengths, E*I, R, LM)
        analysis.analyze()
        
        # ดึงผลลัพธ์จากการวิเคราะห์
        results = analysis.beam_results.results
        x_points = np.array(results.x)  # จุดที่คำนวณผลลัพธ์
        
        # ดึงค่าแรงเฉือน โมเมนต์ดัด และการแอ่นตัว
        shear = np.array(results.V)
        moment = np.array(results.M)
        deflection = np.array(results.D) * 1000  # แปลงเป็น mm
        
        with col2:
            st.subheader("ผลการวิเคราะห์")
            
            # แผนภาพคาน
            fig_beam = go.Figure()
            
            # วาดเส้นคาน
            current_x = 0
            y_base = 0
            
            # คำนวณสเกลแยกสำหรับ UDL และ Point Load
            udl_scale = max([span['udl'] for span in spans_data]) if any(span['udl'] > 0 for span in spans_data) else 1.0
            pl_scale = max([span['pl'] for span in spans_data]) if any(span['pl'] > 0 for span in spans_data) else 1.0
            
            # กำหนดสเกลสำหรับการแสดงผล
            udl_y_scale = udl_scale * 0.15  # สเกลสำหรับน้ำหนักแผ่กระจาย
            pl_y_scale = pl_scale * 0.3   # สเกลสำหรับน้ำหนักจุด
            support_scale = min(udl_y_scale, pl_y_scale) * 0.5  # สเกลสำหรับจุดรองรับ
            
            # วาดเส้นคาน
            beam_points_x = []
            beam_points_y = []
            
            for i, span in enumerate(spans_data):
                # เพิ่มจุดเริ่มต้นช่วงคาน
                beam_points_x.extend([current_x])
                beam_points_y.extend([y_base])
                
                # เพิ่มจุดสิ้นสุดช่วงคาน
                beam_points_x.extend([current_x + span['length']])
                beam_points_y.extend([y_base])
                
                # วาดสัญลักษณ์จุดรองรับ
                if i == 0:  # จุดรองรับแรก
                    fig_beam.add_trace(go.Scatter(x=[current_x], y=[y_base-support_scale],
                                                mode='markers+text',
                                                marker=dict(symbol='triangle-up', size=15),
                                                text=['▲'],
                                                name='Fixed Support'))
                elif i == num_spans-1:  # จุดรองรับสุดท้าย
                    fig_beam.add_trace(go.Scatter(x=[current_x + span['length']], y=[y_base-support_scale],
                                                mode='markers+text',
                                                marker=dict(symbol='triangle-up', size=15),
                                                text=['▲'],
                                                name='Fixed Support'))
                else:  # จุดรองรับกลาง
                    fig_beam.add_trace(go.Scatter(x=[current_x], y=[y_base-support_scale],
                                                mode='markers',
                                                marker=dict(symbol='triangle-up', size=15),
                                                name='Pinned Support'))
                
                # วาด UDL ถ้ามี
                if span['udl'] != 0:
                    arrow_x = np.linspace(current_x, current_x + span['length'], 11)
                    # วาดลูกศรและเส้น UDL
                    for x in arrow_x:
                        fig_beam.add_trace(go.Scatter(x=[x, x], 
                                                    y=[y_base, y_base + udl_y_scale],
                                                    mode='lines',
                                                    line=dict(color='red'),
                                                    showlegend=False))
                        # แสดงลูกศรที่ปลายเส้น
                        fig_beam.add_trace(go.Scatter(x=[x], 
                                                    y=[y_base + udl_y_scale],
                                                    mode='text',
                                                    text=["↓"],
                                                    textposition='top center',
                                                    showlegend=False))
                    # แสดงค่าน้ำหนัก UDL ที่กึ่งกลางช่วง
                    fig_beam.add_trace(go.Scatter(x=[(current_x + span['length'])/2], 
                                                y=[y_base + udl_y_scale * 1.2],
                                                mode='text',
                                                text=[f"{span['udl']} kN/m"],
                                                textposition='top center',
                                                showlegend=False))
                
                # วาด Point Load ถ้ามี
                if span['pl'] != 0:
                    pl_x = current_x + span['pl_location']
                    # วาดเส้นของแรง
                    fig_beam.add_trace(go.Scatter(x=[pl_x, pl_x],
                                                y=[y_base, y_base + pl_y_scale],
                                                mode='lines',
                                                line=dict(color='blue'),
                                                name='Point Load'))
                    # แสดงลูกศร
                    fig_beam.add_trace(go.Scatter(x=[pl_x],
                                                y=[y_base + pl_y_scale],
                                                mode='text',
                                                text=["↓"],
                                                textposition='top center',
                                                showlegend=False))
                    # แสดงค่าน้ำหนัก
                    fig_beam.add_trace(go.Scatter(x=[pl_x],
                                                y=[y_base + pl_y_scale * 1.2],
                                                mode='text',
                                                text=[f"{span['pl']} kN"],
                                                textposition='top center',
                                                showlegend=False))
                
                # เพิ่มระยะช่วงคาน
                fig_beam.add_trace(go.Scatter(x=[current_x + span['length']/2],
                                            y=[y_base - support_scale * 1.6],
                                            mode='text',
                                            text=[f"{span['length']} m"],
                                            showlegend=False))
                
                current_x += span['length']
            
            # วาดเส้นคาน
            fig_beam.add_trace(go.Scatter(x=beam_points_x, y=beam_points_y,
                                        mode='lines',
                                        line=dict(color='black', width=2),
                                        name='Beam'))
            
            # ปรับแต่งกราฟ
            # คำนวณช่วงแกน y
            max_y_scale = max(udl_y_scale, pl_y_scale)
            fig_beam.update_layout(title='แผนภาพคาน',
                                 xaxis_title='ระยะ (m)',
                                 yaxis_title='',
                                 showlegend=True,
                                 yaxis_range=[y_base-max_y_scale, y_base+max_y_scale*1.5])
            st.plotly_chart(fig_beam, use_container_width=True)
            
            # แผนภาพแรงเฉือน
            fig_shear = go.Figure()
            # เพิ่มพื้นที่ใต้กราฟ
            fig_shear.add_trace(go.Scatter(x=x_points, y=shear,
                                         fill='tozeroy',
                                         fillcolor='rgba(0,255,0,0.2)',
                                         line=dict(color='green', width=2),
                                         name='แรงเฉือน',
                                         mode='lines'))
            fig_shear.update_layout(title='แผนภาพแรงเฉือน (kN)',
                                  xaxis_title='ระยะ (m)',
                                  yaxis_title='แรงเฉือน (kN)',
                                  showlegend=True)
            st.plotly_chart(fig_shear, use_container_width=True)
            
            # แผนภาพโมเมนต์ดัด
            fig_moment = go.Figure()
            # เพิ่มพื้นที่ใต้กราฟ
            fig_moment.add_trace(go.Scatter(x=x_points, y=moment,
                                          fill='tozeroy',
                                          fillcolor='rgba(0,150,255,0.2)',
                                          line=dict(color='rgb(0,150,255)', width=2),
                                          name='โมเมนต์ดัด',
                                          mode='lines'))
            fig_moment.update_layout(title='แผนภาพโมเมนต์ดัด (kN·m)',
                                   xaxis_title='ระยะ (m)',
                                   yaxis_title='โมเมนต์ดัด (kN·m)',
                                   showlegend=True)
            st.plotly_chart(fig_moment, use_container_width=True)
            
            # แผนภาพการแอ่นตัว
            fig_defl = go.Figure()
            fig_defl.add_trace(go.Scatter(x=x_points, y=deflection, mode='lines', name='Deflection'))
            fig_defl.update_layout(title='แผนภาพการแอ่นตัว (mm)',
                                 xaxis_title='ระยะ (m)',
                                 yaxis_title='การแอ่นตัว (mm)')
            st.plotly_chart(fig_defl, use_container_width=True)
            
            # แสดงค่าสูงสุด
            col3, col4, col5 = st.columns(3)
            with col3:
                st.metric("แรงเฉือนสูงสุด", f"{max(abs(min(shear)), abs(max(shear))):.2f} kN")
            with col4:
                st.metric("โมเมนต์ดัดสูงสุด", f"{max(abs(min(moment)), abs(max(moment))):.2f} kN·m")
            with col5:
                st.metric("การแอ่นตัวสูงสุด", f"{abs(min(deflection)):.2f} mm")
                
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {str(e)}")