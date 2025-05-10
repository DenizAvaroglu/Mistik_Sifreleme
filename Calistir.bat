@echo off
echo Şifreleme Uygulaması Başlatılıyor...
echo Gerekli kütüphaneler kontrol ediliyor...

python -m pip install -r requirements.txt

echo Uygulama başlatılıyor...
python ŞifrelemeHVS.py

pause 