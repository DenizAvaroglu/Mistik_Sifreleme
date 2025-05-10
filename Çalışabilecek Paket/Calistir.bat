@echo off
echo Sifreleme Uygulamasi Baslatiliyor...
echo Gerekli kutuphaneler kontrol ediliyor...

py -m pip install -r requirements.txt

echo Uygulama baslatiliyor...
py SifrelemeHVS.py

pause 