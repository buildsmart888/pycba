@echo off
cls
echo ================================================================
echo         🌐 PyCBA Google Deployment Guide 🌐
echo ================================================================
echo.
echo เลือกวิธีการ Deploy ที่ต้องการ:
echo.
echo 1. 🚀 Streamlit Community Cloud (ฟรี - แนะนำ)
echo 2. ☁️  Google Cloud Run (มีค่าใช้จ่าย)
echo 3. 🌐 Google Sites + Embed
echo 4. ❓ ดูคำแนะนำทั้งหมด
echo.
set /p choice="เลือก (1-4): "

if "%choice%"=="1" goto streamlit_cloud
if "%choice%"=="2" goto google_cloud
if "%choice%"=="3" goto google_sites
if "%choice%"=="4" goto show_guide
goto invalid_choice

:streamlit_cloud
cls
echo ================================================================
echo           🚀 Streamlit Community Cloud (ฟรี!)
echo ================================================================
echo.
echo ขั้นตอนการ Deploy:
echo.
echo 1. Push โค้ดขึ้น GitHub repository
echo 2. ไปที่ https://share.streamlit.io
echo 3. เข้าสู่ระบบด้วย GitHub account
echo 4. คลิก "New app"
echo 5. เลือก repository: pycba
echo 6. เลือกไฟล์: advanced_app.py
echo 7. คลิก "Deploy!"
echo.
echo URL ที่จะได้:
echo https://buildsmart888-pycba-advanced-app-main.streamlit.app
echo.
echo ✅ ข้อดี: ฟรี, ง่าย, Auto-deploy, HTTPS
echo ❌ ข้อเสีย: Public เท่านั้น, จำกัด resources
echo.
start https://share.streamlit.io
echo เปิด Streamlit Cloud ในเบราว์เซอร์แล้ว...
goto end

:google_cloud
cls
echo ================================================================
echo              ☁️ Google Cloud Run Deployment
echo ================================================================
echo.
echo ขั้นตอนการ Deploy:
echo.
echo 1. ติดตั้ง Google Cloud CLI
echo 2. สร้าง Google Cloud Project
echo 3. Enable APIs (Cloud Build, Cloud Run)
echo 4. Build container image
echo 5. Deploy to Cloud Run
echo.
echo ค่าใช้จ่ายประมาณ: $0-10/เดือน
echo.
echo ✅ ข้อดี: Scalable, Custom domain, Private access
echo ❌ ข้อเสีย: มีค่าใช้จ่าย, ซับซ้อนกว่า
echo.
set /p confirm="ต้องการรัน deployment script? (y/n): "
if /i "%confirm%"=="y" (
    echo.
    echo เรียกใช้ Google Cloud deployment script...
    call deploy-google-cloud.bat
) else (
    echo.
    echo สำหรับรายละเอียด: ดูไฟล์ GOOGLE-DEPLOYMENT.md
    start GOOGLE-DEPLOYMENT.md
)
goto end

:google_sites
cls
echo ================================================================
echo             🌐 Google Sites Integration
echo ================================================================
echo.
echo ขั้นตอนการใส่ใน Google Sites:
echo.
echo 1. Deploy แอปบน Streamlit Cloud ก่อน (วิธีที่ 1)
echo 2. Copy URL ของแอป
echo 3. เข้า Google Sites
echo 4. สร้าง New Site
echo 5. เพิ่ม "Embed" component
echo 6. วาง URL ของแอป
echo 7. ตั้งค่า iframe size
echo.
echo ไฟล์ตัวอย่าง: google-sites-embed.html
echo.
echo ✅ ข้อดี: รวมกับ Google Sites ได้, ง่าย
echo ❌ ข้อเสีย: ต้อง deploy แอปแยกก่อน
echo.
start https://sites.google.com
echo เปิด Google Sites ในเบราว์เซอร์แล้ว...
echo.
echo ดูตัวอย่าง HTML embed code:
start google-sites-embed.html
goto end

:show_guide
cls
echo ================================================================
echo                  📚 Complete Deployment Guide
echo ================================================================
echo.
echo เปิดไฟล์คำแนะนำทั้งหมด:
echo.
start GOOGLE-DEPLOYMENT.md
start DEPLOYMENT.md
echo.
echo ไฟล์ที่เกี่ยวข้อง:
echo - GOOGLE-DEPLOYMENT.md (Google specific guide)
echo - DEPLOYMENT.md (Complete deployment options)
echo - google-sites-embed.html (HTML embed template)
echo - deploy-google-cloud.bat (Google Cloud script)
echo.
goto end

:invalid_choice
echo.
echo ❌ กรุณาเลือกตัวเลข 1-4
pause
goto start

:end
echo.
echo ================================================================
echo                     🎉 ขอให้โชคดี! 🎉
echo ================================================================
echo.
echo 📞 หากต้องการความช่วยเหลือ:
echo    - ดูไฟล์ GOOGLE-DEPLOYMENT.md
echo    - Check GitHub Issues
echo    - ติดต่อทีมพัฒนา
echo.
echo Press any key to exit...
pause >nul
