@echo off
echo Sifreleme Programi Kurulum ve Calistirma
echo ========================================
echo.

REM Python'un kurulu olup olmadigini kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo Python kurulu degil! Lutfen Python'u kurun.
    echo https://www.python.org/downloads/
    pause
    exit
)

REM Gerekli paketleri kur
echo Gerekli paketler kuruluyor...
pip install -r requirements.txt

REM Programi calistir
echo.
echo Program baslatiliyor...
python SifrelemeHVS.py

pause 