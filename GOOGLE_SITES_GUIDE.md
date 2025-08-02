# 🌐 Google Sites Integration Guide

## วิธีการนำ PyCBA Suite ขึ้น Google Sites

### วิธีที่ 1: Streamlit Community Cloud (ฟรี + แนะนำ)

#### ขั้นตอน Deploy บน Streamlit Cloud:

1. **เตรียม GitHub Repository**
   ```bash
   # Push code ไปยัง GitHub
   git add .
   git commit -m "Add PyCBA Suite with home page"
   git push origin main
   ```

2. **Deploy บน Streamlit Cloud**
   - ไปที่ [share.streamlit.io](https://share.streamlit.io)
   - Sign in ด้วย GitHub account
   - Click "New app"
   - เลือก Repository: `buildsmart888/pycba`
   - กำหนด Main file path: `home.py`
   - กำหนด URL: `pycba-engineering-suite` (หรือชื่อที่ต้องการ)
   - Click "Deploy"

3. **รอการ Deploy เสร็จ** (ประมาณ 2-3 นาที)
   - ระบบจะสร้าง URL อัตโนมัติ: `https://pycba-engineering-suite.streamlit.app`

#### ขั้นตอนเพิ่มใน Google Sites:

1. **เปิด Google Sites**
   - ไปที่ [sites.google.com](https://sites.google.com)
   - สร้างเว็บไซต์ใหม่หรือแก้ไขเว็บที่มีอยู่

2. **เพิ่ม Embed Element**
   - Click "Insert" → "Embed"
   - เลือก "Embed code"
   - วางโค้ดนี้:

   ```html
   <iframe src="https://pycba-engineering-suite.streamlit.app" 
           width="100%" 
           height="800" 
           frameborder="0"
           style="border: none; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
   </iframe>
   ```

3. **Publish เว็บไซต์**
   - Click "Publish" ที่มุมขวาบน
   - เลือก URL สำหรับเว็บไซต์
   - เว็บจะใช้งานได้ทันที

---

### วิธีที่ 2: Google Cloud Run (สำหรับ Professional)

#### Deploy ด้วย Google Cloud Run:

1. **เตรียม Google Cloud Project**
   ```bash
   # ติดตั้ง gcloud CLI
   # สร้าง project ใหม่หรือใช้ที่มีอยู่
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Deploy Application**
   ```bash
   # ไปยังโฟลเดอร์โปรเจ็ค
   cd /path/to/pycba
   
   # Deploy ไปยัง Cloud Run
   gcloud run deploy pycba-suite \
     --source . \
     --platform managed \
     --region asia-southeast1 \
     --allow-unauthenticated \
     --port 8501
   ```

3. **รับ URL จาก Cloud Run**
   - หลังจาก deploy สำเร็จ จะได้ URL เช่น:
   - `https://pycba-suite-xxxxxxxxx-as.a.run.app`

4. **นำ URL ไปใช้ใน Google Sites** (เหมือนวิธีที่ 1)

---

### วิธีที่ 3: GitHub Pages + Netlify (Alternative)

#### สำหรับหน้า Landing Page:

1. **Deploy หน้า Portfolio บน GitHub Pages**
   - Copy `google-sites-portfolio.html` เป็น `index.html`
   - Push ไป GitHub Repository
   - เปิด GitHub Pages ใน Settings

2. **ได้ URL:** `https://buildsmart888.github.io/pycba`

3. **นำไปใช้ใน Google Sites**
   ```html
   <iframe src="https://buildsmart888.github.io/pycba" 
           width="100%" 
           height="600">
   </iframe>
   ```

---

## 🎨 ปรับแต่ง Google Sites

### Theme และการจัดวาง:

1. **เลือก Theme ที่เหมาะสม**
   - Simple, Modern หรือ Academic
   - สีที่เข้ากับ PyCBA (น้ำเงิน-ม่วง)

2. **จัดเรียงเนื้อหา**
   ```
   หน้าแรก
   ├── Header: "PyCBA Engineering Suite"
   ├── Navigation Menu
   ├── PyCBA Embed (iframe)
   ├── Description
   └── Contact Information
   ```

3. **เพิ่ม Navigation**
   - Home
   - โปรแกรมวิศวกรรม (PyCBA)
   - บทความ/Tutorials
   - ติดต่อ

### เพิ่มเนื้อหาเสริม:

```html
<!-- ก่อนหน้า iframe -->
<div style="text-align: center; margin: 20px 0;">
    <h2>🏗️ ชุดโปรแกรมวิศวกรรมโครงสร้าง</h2>
    <p>เครื่องมือวิเคราะห์โครงสร้างที่ทันสมัย สำหรับวิศวกรและนักศึกษา</p>
</div>

<!-- หลัง iframe -->
<div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
    <h3>คุณสมบัติเด่น</h3>
    <ul>
        <li>✅ วิเคราะห์คานต่อเนื่องแม่นยำ</li>
        <li>✅ แสดงผลแผนภาพโครงสร้าง</li>
        <li>✅ ใช้งานผ่าน Web Browser</li>
        <li>✅ ไม่ต้องติดตั้งโปรแกรม</li>
    </ul>
</div>
```

---

## 📊 Monitoring และ Analytics

### Google Analytics สำหรับ Streamlit:

```python
# เพิ่มใน home.py
import streamlit as st

# Google Analytics
st.components.v1.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", height=0)
```

### ติดตามการใช้งาน:
- Page views ใน Google Sites
- App usage ใน Streamlit
- User engagement metrics

---

## 🔧 Troubleshooting

### ปัญหาที่พบบ่อย:

1. **iframe ไม่แสดงผล**
   - ตรวจสอบ URL ถูกต้อง
   - ตรวจสอบ HTTPS/HTTP
   - ลองใช้ height ที่มากกว่า

2. **App โหลดช้า**
   - Streamlit Community Cloud อาจมี cold start
   - พิจารณาใช้ Google Cloud Run

3. **บางฟีเจอร์ไม่ทำงาน**
   - ตรวจสอบ dependencies ใน requirements.txt
   - ดู logs ใน Streamlit Cloud

### วิธีแก้ไข:

```bash
# ตรวจสอบ logs
streamlit run home.py --logger.level=debug

# ทดสอบ local ก่อน deploy
streamlit run home.py --server.port=8501
```

---

## 🎯 Best Practices

1. **Performance**
   - ใช้ st.cache_data สำหรับการคำนวณ
   - Optimize image sizes
   - Minimize dependencies

2. **User Experience**
   - เพิ่ม loading indicators
   - Error handling ที่ดี
   - Mobile-friendly design

3. **SEO**
   - เพิ่ม meta descriptions
   - ใช้ structured data
   - Optimize page titles

4. **Security**
   - ไม่เก็บข้อมูลส่วนตัว
   - ใช้ HTTPS
   - Regular updates

---

## 📞 Support

หากมีปัญหาในการ Deploy:

1. **Documentation**
   - [Streamlit Documentation](https://docs.streamlit.io)
   - [Google Sites Help](https://support.google.com/sites)

2. **Community**
   - Streamlit Community Forum
   - GitHub Issues

3. **Contact**
   - Email: support@pycba.com
   - GitHub: buildsmart888/pycba
