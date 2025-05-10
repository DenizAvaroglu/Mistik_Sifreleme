# -*- coding: utf-8 -*-
import sys
import os
import math
import base64
import subprocess
import tempfile
import shutil
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                QHBoxLayout, QComboBox, QLineEdit, QTextEdit, 
                                QPushButton, QLabel, QFileDialog, QTabWidget, QMessageBox)
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
except ImportError:
    print("PyQt5 modülü bulunamadı. Lütfen 'pip install PyQt5==5.15.9' komutunu çalıştırarak yükleyin.")
    input("Çıkmak için ENTER tuşuna basın...")
    sys.exit(1)


# WinRAR yolunu tanımlayalım
WINRAR_PATH = "C:\\Program Files\\WinRAR\\WinRAR.exe"
# Alternatif WinRAR yolları
ALTERNATIVE_WINRAR_PATHS = [
    "C:\\Program Files (x86)\\WinRAR\\WinRAR.exe",
    "C:\\Program Files\\WinRAR\\WinRAR.exe", 
    "C:\\WinRAR\\WinRAR.exe"
]

class SifrelemeFormu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifreleme Uygulaması")
        self.setGeometry(100, 100, 800, 600)
        
        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Tab widget oluştur
        self.tabs = QTabWidget()
        self.sifreleme_tab = QWidget()
        self.cozme_tab = QWidget()
        
        self.tabs.addTab(self.sifreleme_tab, "Şifreleme")
        self.tabs.addTab(self.cozme_tab, "Çözme")
        
        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.central_widget.setLayout(main_layout)
        
        # WinRAR varlığını kontrol et
        self.check_winrar()
        
        # Şifreleme sekmesini ayarla
        self.setup_sifreleme_tab()
        
        # Çözme sekmesini ayarla
        self.setup_cozme_tab()
    
    def check_winrar(self):
        """WinRAR programının varlığını kontrol eder"""
        global WINRAR_PATH
        
        # Önce default konumu kontrol et
        if os.path.exists(WINRAR_PATH):
            return True
        
        # Alternatif yolları kontrol et
        for path in ALTERNATIVE_WINRAR_PATHS:
            if os.path.exists(path):
                WINRAR_PATH = path
                return True
            
        # WinRAR bulunamadı
        QMessageBox.warning(self, "Uyarı", 
            "WinRAR bulunamadı!\n\n"
            "Lütfen WinRAR programının kurulu olduğundan emin olun.\n"
            "Varsayılan konum: C:\\Program Files\\WinRAR\\WinRAR.exe")
        return False
    
    def setup_sifreleme_tab(self):
        layout = QVBoxLayout()
        
        # Üst kısım için ComboBox'lar ve LineEdit'ler
        ust_layout = QHBoxLayout()
        
        # Element Combobox
        element_layout = QVBoxLayout()
        element_label = QLabel("Element:")
        self.element_combo = QComboBox()
        self.element_combo.addItems(["Ateş", "Su", "Toprak", "Hava"])
        element_layout.addWidget(element_label)
        element_layout.addWidget(self.element_combo)
        ust_layout.addLayout(element_layout)
        
        # Derece Combobox
        derece_layout = QVBoxLayout()
        derece_label = QLabel("Derece:")
        self.derece_combo = QComboBox()
        self.derece_combo.addItems(["30", "60", "90", "120", "180"])
        derece_layout.addWidget(derece_label)
        derece_layout.addWidget(self.derece_combo)
        ust_layout.addLayout(derece_layout)
        
        # Satır Sayısı Combobox
        satir_layout = QVBoxLayout()
        satir_label = QLabel("Satır Sayısı:")
        self.satir_combo = QComboBox()
        self.satir_combo.addItems(["1", "2", "3", "4", "5", "6", "7"])
        satir_layout.addWidget(satir_label)
        satir_layout.addWidget(self.satir_combo)
        ust_layout.addLayout(satir_layout)
        
        # Başlık Text Box
        baslik_layout = QVBoxLayout()
        baslik_label = QLabel("Başlık:")
        self.baslik_text = QLineEdit()
        baslik_layout.addWidget(baslik_label)
        baslik_layout.addWidget(self.baslik_text)
        ust_layout.addLayout(baslik_layout)
        
        # Sayı Text Box
        sayi_layout = QVBoxLayout()
        sayi_label = QLabel("Sayı:")
        self.sayi_text = QLineEdit()
        sayi_layout.addWidget(sayi_label)
        sayi_layout.addWidget(self.sayi_text)
        ust_layout.addLayout(sayi_layout)
        
        layout.addLayout(ust_layout)
        
        # Rich Text Box
        text_label = QLabel("Metin:")
        self.rich_text = QTextEdit()
        self.rich_text.setMinimumHeight(200)
        layout.addWidget(text_label)
        layout.addWidget(self.rich_text)
        
        # Butonlar
        butonlar_layout = QHBoxLayout()
        self.metin_donustur_btn = QPushButton("Metni Dönüştür")
        self.sifrele_btn = QPushButton("Şifrele")
        
        butonlar_layout.addWidget(self.metin_donustur_btn)
        butonlar_layout.addWidget(self.sifrele_btn)
        layout.addLayout(butonlar_layout)
        
        # Şifre ve sonuç alanı
        sonuc_label = QLabel("Şifre:")
        self.sonuc_text = QLineEdit()
        self.sonuc_text.setReadOnly(True)
        layout.addWidget(sonuc_label)
        layout.addWidget(self.sonuc_text)
        
        # Butonların bağlantıları
        self.metin_donustur_btn.clicked.connect(self.metin_donustur)
        self.sifrele_btn.clicked.connect(self.sifrele)
        
        self.sifreleme_tab.setLayout(layout)
    
    def setup_cozme_tab(self):
        layout = QVBoxLayout()
        
        # Dosya seçme bölümü
        dosya_secimi_layout = QHBoxLayout()
        self.dosya_yolu_text = QLineEdit()
        self.dosya_yolu_text.setReadOnly(True)
        self.dosya_sec_btn = QPushButton("Dosya Seç")
        self.dosya_sec_btn.clicked.connect(self.dosya_sec)
        
        dosya_secimi_layout.addWidget(QLabel("Şifreli Dosya:"))
        dosya_secimi_layout.addWidget(self.dosya_yolu_text)
        dosya_secimi_layout.addWidget(self.dosya_sec_btn)
        layout.addLayout(dosya_secimi_layout)
        
        # Otomatik Çözme Butonu - İsmi değiştirildi
        self.otomatik_coz_btn = QPushButton("Çözümle")
        self.otomatik_coz_btn.setMinimumHeight(50) 
        self.otomatik_coz_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.otomatik_coz_btn.clicked.connect(self.otomatik_coz)
        layout.addWidget(self.otomatik_coz_btn)
        
        # Bilgi alanı - Word wrap özelliği ve esnek yükseklik, uzun şifreler için düzenlendi
        self.bilgi_label = QLabel("Dosya seçin ve çözümle butonuna tıklayın")
        self.bilgi_label.setAlignment(Qt.AlignCenter)
        self.bilgi_label.setWordWrap(True)  # Metni otomatik alt satıra geçirmek için
        self.bilgi_label.setMinimumHeight(60)  # Minimum yükseklik, içerik büyüdükçe otomatik genişleyecek
        self.bilgi_label.setMaximumHeight(150)  # Maksimum yükseklik, çok uzun olmasını engellemek için
        self.bilgi_label.setStyleSheet("background-color: #f0f0f0; padding: 5px; border-radius: 5px;")
        layout.addWidget(self.bilgi_label)
        
        # Çözülmüş metin
        cozulmus_label = QLabel("Çözülmüş Metin:")
        self.cozulmus_text = QTextEdit()
        self.cozulmus_text.setReadOnly(True)
        layout.addWidget(cozulmus_label)
        layout.addWidget(self.cozulmus_text)
        
        self.cozme_tab.setLayout(layout)
    
    def metin_donustur(self):
        metin = self.rich_text.toPlainText()
        if not metin:
            QMessageBox.warning(self, "Uyarı", "Metin boş olamaz!")
            return
            
        # Satır sayısını al
        satir_sayisi = int(self.satir_combo.currentText())
        
        if len(metin) < 2:
            QMessageBox.warning(self, "Uyarı", "Metin en az 2 karakter olmalıdır!")
            return
        
        # 1. Adım: Metni bir son bir baş şeklinde düzenle
        duzenlenmis_metin = self.bir_son_bir_bas(metin)
        
        # 2. Adım: Metni satırlara böl
        satirlar = self.metni_satirlara_bol(duzenlenmis_metin, satir_sayisi)
        
        # 3. Adım: Her satırı kendi içinde bir son bir baş şeklinde düzenle
        son_satirlar = []
        for satir in satirlar:
            son_satirlar.append(self.bir_son_bir_bas(satir))
        
        # 4. Adım: Satırları birleştir
        son_metin = ''.join(son_satirlar)
        
        # Sonucu Rich Text Box'a yaz
        self.rich_text.setPlainText(son_metin)
    
    def bir_son_bir_bas(self, metin):
        """Metni bir sondan bir baştan olacak şekilde düzenler"""
        if len(metin) <= 1:
            return metin
        
        yeni_metin = ""
        i_bas = 0
        i_son = len(metin) - 1
        
        while i_bas <= i_son:
            if i_bas == i_son:  # Ortadaki tek karakter
                yeni_metin += metin[i_bas]
                break
            
            # Önce sondan, sonra baştan
            yeni_metin += metin[i_son] + metin[i_bas]
            i_bas += 1
            i_son -= 1
            
        return yeni_metin
    
    def metni_satirlara_bol(self, metin, satir_sayisi):
        """Metni belirtilen satır sayısına göre böler"""
        if satir_sayisi <= 1:
            return [metin]
        
        karakter_sayisi = len(metin)
        # Eşit uzunlukta satırlar oluşturmaya çalışalım
        satir_basina_karakter = math.ceil(karakter_sayisi / satir_sayisi)
        
        satirlar = []
        for i in range(0, karakter_sayisi, satir_basina_karakter):
            son_index = min(i + satir_basina_karakter, karakter_sayisi)
            satirlar.append(metin[i:son_index])
        
        # Eğer istenen satır sayısı kadar oluşmamışsa, kalan satırları ekle
        while len(satirlar) < satir_sayisi:
            satirlar.append("")
        
        # Fazla satır varsa, birleştir
        while len(satirlar) > satir_sayisi:
            satirlar[-2] += satirlar[-1]
            satirlar.pop()
        
        return satirlar
    
    def sifrele(self):
        metin = self.rich_text.toPlainText()
        baslik = self.baslik_text.text()
        sayi_text = self.sayi_text.text()
        
        if not metin or not baslik or not sayi_text:
            QMessageBox.warning(self, "Uyarı", "Tüm alanlar doldurulmalıdır!")
            return
            
        try:
            sayi = int(sayi_text)
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir sayı girin!")
            return
            
        # Element ve derece değerlerini al
        element = self.element_combo.currentText()
        derece = int(self.derece_combo.currentText())
        satir_sayisi = int(self.satir_combo.currentText())
        
        # Dereceye göre hesaplama
        if derece == 30:
            cikarilacak = 12
            artis = 1
        elif derece == 60:
            cikarilacak = 24
            artis = 2
        elif derece == 90:
            cikarilacak = 36
            artis = 3
        elif derece == 120:
            cikarilacak = 48
            artis = 4
        elif derece == 150:
            cikarilacak = 60
            artis = 5
        else:  # 180
            cikarilacak = 72
            artis = 6
            
        hesaplanan = sayi - cikarilacak
        if hesaplanan < 0:
            QMessageBox.warning(self, "Uyarı", f"Sayı {cikarilacak}'den küçük olamaz!")
            return
            
        bolum = hesaplanan // 3
        kalan = hesaplanan % 3
        
        # 9 sayı hesaplama
        sayilar = []
        for i in range(9):
            if i == 0:
                sayilar.append(bolum)
            elif i == 6 and kalan > 0:  # 7. sayı (0-indeksli 6) kalan eklenir
                sayilar.append(bolum + (i * artis) + kalan)
            else:
                sayilar.append(bolum + (i * artis))
        
        # Elemente göre sıralama
        sifreli_sayilar = []
        ebced_değerleri = []  # Ebced değerlerini saklayacak liste
        
        if element == "Toprak":
            siralama = [1, 8, 3, 0, 4, 5, 7, 6, 2]  # 2,9,4,1,5,6,8,7,3
        elif element == "Ateş":
            siralama = [3, 2, 7, 8, 4, 0, 1, 6, 5]  # 4,3,8,9,5,1,2,7,6
        elif element == "Hava":
            siralama = [7, 0, 5, 2, 4, 6, 3, 8, 1]  # 8,1,6,3,5,7,4,9,2
        else:  # Su
            siralama = [5, 6, 1, 0, 4, 8, 7, 2, 3]  # 6,7,2,1,5,9,8,3,4
            
        for idx in siralama:
            if idx < len(sayilar):
                sifreli_sayilar.append(str(sayilar[idx]))
                ebced_değerleri.append(sayilar[idx])  # Ebced dönüşümü için sayıları kaydet
        
        sifre = ''.join(sifreli_sayilar)
        
        # Ebced dönüşümü yapılır ve alternatif şifre oluşturulur
        ebced_sifre = ""
        for i, deger in enumerate(ebced_değerleri):
            ebced_metin = self.sayi_ebced_donusumu(deger)
            ebced_sifre += str(deger) + ebced_metin
        
        # WinRAR için şifreyi düzenle - sadece alfanumerik ve sayılar kalsın
        rar_sifre = ''.join(karakter for karakter in ebced_sifre if karakter.isalnum())
        if not rar_sifre:
            rar_sifre = sifre  # Boşsa orijinal sayısal şifreyi kullan
        
        # Sonuç metin kutusunu güncelle - sadece RAR şifresini göster
        sonuc_metin = f"RAR Şifresi: {rar_sifre}"
        self.sonuc_text.setText(sonuc_metin)
        
        # Dosya adı oluşturma - YENİ FORMAT: [SatırSayısı][ElementHarf][Derece],[Sayı]_[Başlık]
        element_harf = element[0]
        dosya_adi = f"{satir_sayisi}{element_harf}{derece},{sayi}_{baslik}"
        
        # Masaüstü yolu
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop") 
            if not os.path.exists(desktop):
                desktop = os.path.join(os.path.expanduser("~"), "Masaüstü")
        except:
            desktop = os.path.expanduser("~")  # Fallback olarak kullanıcı dizini
        
        # Metin dosyasını oluştur ve şifrele
        # Geçici klasörü temizleyerek işleme başla
        temp_dir = os.path.join(tempfile.gettempdir(), "sifreleme_temp")
        
        # Önceki temp klasörünü temizle
        if os.path.exists(temp_dir):
            try:
                for dosya in os.listdir(temp_dir):
                    dosya_yol = os.path.join(temp_dir, dosya)
                    if os.path.isfile(dosya_yol):
                        os.remove(dosya_yol)
                    elif os.path.isdir(dosya_yol):
                        shutil.rmtree(dosya_yol, ignore_errors=True)
            except Exception as e:
                print(f"Temp klasörü temizlenirken hata: {e}")
        
        # Klasörü oluştur
        os.makedirs(temp_dir, exist_ok=True)
        
        # Metni şifrelemek için Base64 kullanıyoruz ve yapılan tüm işlem bilgilerini ekliyoruz
        metadata = f"SATIR:{satir_sayisi}\nELEMENT:{element}\nDERECE:{derece}\nSAYI:{sayi}\nALTERNATIF_SIFRE:{ebced_sifre}\n"
        encoded_data = base64.b64encode((metadata + metin).encode('utf-8')).decode('utf-8')
        
        txt_yolu = os.path.join(temp_dir, f"{baslik}.txt")
        with open(txt_yolu, "w", encoding="utf-8") as f:
            f.write(encoded_data)
        
        # Dosyanın varlığını kontrol et
        if not os.path.exists(txt_yolu):
            QMessageBox.critical(self, "Hata", f"Metin dosyası oluşturulamadı: {txt_yolu}")
            return
            
        # RAR dosyası oluştur
        rar_yolu = os.path.join(desktop, f"{dosya_adi}.rar")
        
        # WinRAR varlığını kontrol et
        if not os.path.exists(WINRAR_PATH):
            QMessageBox.critical(self, "Hata", f"WinRAR bulunamadı: {WINRAR_PATH}")
            return
            
        # WinRAR komutu kullanarak şifreli RAR oluştur
        try:
            # Çift tırnak ve ekstra karakterlerden kaçınmak için yolları düzeltiyoruz
            txt_yolu_duzeltilmis = f'"{txt_yolu}"'
            rar_yolu_duzeltilmis = f'"{rar_yolu}"'
            
            # Komut satırı - Düzenlenmiş şifreyi kullan
            rar_komut = f'"{WINRAR_PATH}" a -ep -p{rar_sifre} {rar_yolu_duzeltilmis} {txt_yolu_duzeltilmis}'
            
            # Komutu göster (hata ayıklama için)
            print(f"Çalıştırılan komut: {rar_komut}")
            
            # Komutu çalıştır
            process = subprocess.run(rar_komut, shell=True, capture_output=True, text=True)
            
            if process.returncode != 0:
                error_msg = process.stderr if process.stderr else "Bilinmeyen hata"
                print(f"WinRAR çıktısı: {process.stdout}")
                print(f"WinRAR hatası: {process.stderr}")
                raise Exception(f"WinRAR hatası: {error_msg}")
                
            QMessageBox.information(self, "Bilgi", 
                f"Şifreleme başarılı! RAR dosyası kaydedildi: {rar_yolu}\n\n"
                f"Dosya adı: {dosya_adi}.rar\n"
                f"RAR Şifresi: {rar_sifre}")
                
            # İşlem tamamlanınca geçici dosyaları temizle
            try:
                os.remove(txt_yolu)
            except:
                pass
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"RAR dosyası oluşturulamadı: {str(e)}")

    def dosya_sec(self):
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Şifreli Dosya Seç", "", "RAR Dosyaları (*.rar)")
        if dosya_yolu:
            self.dosya_yolu_text.setText(dosya_yolu)
            # Dosya adından bilgileri otomatik çıkar ve göster
            bilgiler = self.dosya_bilgilerini_al(dosya_yolu)
            if bilgiler:
                satir, element, derece, sayi = bilgiler
                self.bilgi_label.setText(f"Algılanan: Satır: {satir}, Element: {element}, Derece: {derece}, Sayı: {sayi}")
            else:
                self.bilgi_label.setText("Dosya adı formatı uygun değil! Format: [SatırSayısı][ElementHarfi][Derece],[Sayı]_[Başlık].rar")
    
    def dosya_bilgilerini_al(self, dosya_yolu):
        """Dosya adından satır sayısı, element, derece ve sayı bilgilerini çıkarır"""
        try:
            dosya_adi = os.path.basename(dosya_yolu)
            dosya_adi = os.path.splitext(dosya_adi)[0]  # .rar uzantısını kaldır
            
            # Dosya adından elementi, dereceyi ve sayıyı al
            if len(dosya_adi) > 0:
                # İlk rakam satır sayısı
                if not dosya_adi[0].isdigit():
                    return None
                    
                satir_sayisi = int(dosya_adi[0])
                element_harf = dosya_adi[1].upper() if len(dosya_adi) > 1 else None
                
                # Element belirleme
                element = None
                if element_harf == "A":
                    element = "Ateş"
                elif element_harf == "S":
                    element = "Su"
                elif element_harf == "T":
                    element = "Toprak"
                elif element_harf == "H":
                    element = "Hava"
                
                # Derece ve sayı alma
                if "," in dosya_adi:
                    parts = dosya_adi.split(",")
                    if len(parts) > 1:
                        # İlk kısımdan derece al
                        derece_str = ""
                        for char in parts[0][2:]:  # Satır ve element harfini atla
                            if char.isdigit():
                                derece_str += char
                            else:
                                break
                        
                        # İkinci kısımdan sayı al
                        ikinci_kisim = parts[1]
                        if "_" in ikinci_kisim:
                            sayi_str = ikinci_kisim.split("_")[0]
                            try:
                                derece = int(derece_str) if derece_str else 0
                                sayi = int(sayi_str) if sayi_str else 0
                                return satir_sayisi, element, derece, sayi
                            except ValueError:
                                pass
            
            return None
        except Exception as e:
            print(f"Dosya bilgilerini çıkarırken hata: {e}")
            return None
    
    def otomatik_coz(self):
        """Dosya adından parametreleri çıkar, şifreyi hesapla ve dosyayı otomatik çöz"""
        dosya_yolu = self.dosya_yolu_text.text()
        if not dosya_yolu:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir dosya seçin!")
            return
            
        # Dosya adından bilgileri al
        bilgiler = self.dosya_bilgilerini_al(dosya_yolu)
        if not bilgiler:
            QMessageBox.warning(self, "Uyarı", "Dosya adından bilgiler çıkarılamadı!")
            return
            
        satir_sayisi, element, derece, sayi = bilgiler
        
        # Şifreyi hesapla
        sifre = self.sifre_hesapla(element, derece, sayi)
        if not sifre:
            return
        
        try:
            # Masaüstü yolu
            try:
                desktop = os.path.join(os.path.expanduser("~"), "Desktop") 
                if not os.path.exists(desktop):
                    desktop = os.path.join(os.path.expanduser("~"), "Masaüstü")
            except:
                desktop = os.path.expanduser("~")  # Fallback olarak kullanıcı dizini
            
            # Geçici dizin oluştur - sistem geçici klasöründe oluştur
            temp_dir = os.path.join(tempfile.gettempdir(), "sifreleme_extract_temp")
            
            # Eğer klasör zaten varsa, içeriğini temizle
            if os.path.exists(temp_dir):
                try:
                    for dosya in os.listdir(temp_dir):
                        dosya_yol = os.path.join(temp_dir, dosya)
                        if os.path.isfile(dosya_yol):
                            os.remove(dosya_yol)
                        elif os.path.isdir(dosya_yol):
                            shutil.rmtree(dosya_yol, ignore_errors=True)
                except Exception as e:
                    print(f"Geçici klasör temizlenirken hata: {e}")
            
            # Klasörü oluştur
            os.makedirs(temp_dir, exist_ok=True)
            
            # RAR dosyasını WinRAR ile aç
            try:
                # WinRAR varlığını kontrol et
                if not os.path.exists(WINRAR_PATH):
                    QMessageBox.critical(self, "Hata", f"WinRAR bulunamadı: {WINRAR_PATH}")
                    return
                
                # Çift tırnak ve ekstra karakterlerden kaçınmak için yolları düzeltiyoruz
                dosya_yolu_duzeltilmis = f'"{dosya_yolu}"'
                temp_dir_duzeltilmis = f'"{temp_dir}\\"'
                
                # Komut satırı
                rar_komut = f'"{WINRAR_PATH}" x -p{sifre} {dosya_yolu_duzeltilmis} {temp_dir_duzeltilmis}'
                
                # Komutu göster (hata ayıklama için)
                print(f"Çalıştırılan komut: {rar_komut}")
                
                # Komutu çalıştır
                process = subprocess.run(rar_komut, shell=True, capture_output=True, text=True)
                
                if process.returncode != 0:
                    error_msg = process.stderr if process.stderr else "Bilinmeyen hata"
                    print(f"WinRAR çıktısı: {process.stdout}")
                    print(f"WinRAR hatası: {process.stderr}")
                    raise Exception(f"WinRAR hatası: {error_msg}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Hata", 
                    f"RAR dosyası açılamadı: {str(e)}")
                return
            
            # İçindeki metin dosyasını bul ve oku
            txt_dosyalari = [f for f in os.listdir(temp_dir) if f.endswith('.txt')]
            if not txt_dosyalari:
                QMessageBox.warning(self, "Uyarı", "RAR içinde metin dosyası bulunamadı!")
                return
                
            txt_yolu = os.path.join(temp_dir, txt_dosyalari[0])
            with open(txt_yolu, 'r', encoding="utf-8") as f:
                encoded_content = f.read()
            
            # Şifrelenmiş içeriği çöz
            try:
                decoded_content = base64.b64decode(encoded_content).decode('utf-8')
                
                # Metadata'yı kontrol et ve çıkar
                metadata_lines = []
                content_start_idx = 0
                
                lines = decoded_content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith("SATIR:") or line.startswith("ELEMENT:") or line.startswith("DERECE:") or line.startswith("SAYI:") or line.startswith("ALTERNATIF_SIFRE:"):
                        metadata_lines.append(line)
                        content_start_idx = i + 1
                    else:
                        break
                
                # Metadatadaki satır bilgisini alalım
                satir_bilgisi = None
                for line in metadata_lines:
                    if line.startswith("SATIR:"):
                        try:
                            satir_bilgisi = int(line.split(':')[1].strip())
                            break
                        except:
                            pass
                
                # Metin içeriğini al
                sifreli_metin = '\n'.join(lines[content_start_idx:])
                
                # Satır bilgisi varsa kullan, yoksa dosya adından alınan değeri kullan
                kullanilacak_satir = satir_bilgisi if satir_bilgisi is not None else satir_sayisi
                
                # Metni satır sayısına göre düzelt
                cozulmus_metin = self.metni_tersine_cevir(sifreli_metin, kullanilacak_satir)
                
                # Alternatif şifreyi al
                alternatif_sifre = ""
                for line in metadata_lines:
                    if line.startswith("ALTERNATIF_SIFRE:"):
                        alternatif_sifre = line.split(":", 1)[1].strip()
                        break
                
                # Metni göster
                self.cozulmus_text.setPlainText(cozulmus_metin)
                
                # Bilgi mesajı güncelle - Formatı düzenlendi, şifre kısaltılmadan tamamı gösteriliyor
                info_text = f"Dosya başarıyla çözüldü!\nSatır: {kullanilacak_satir}, Element: {element}\nDerece: {derece}, Sayı: {sayi}\n"
                if alternatif_sifre:
                    info_text += f"RAR Şifresi:\n{alternatif_sifre}"
                else:
                    info_text += f"RAR Şifresi:\n{sifre}"
                self.bilgi_label.setText(info_text)
                
                # İşlem tamamlandığında geçici dosyaları temizle
                try:
                    os.remove(txt_yolu)
                except:
                    pass
                
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Metin çözülemedi: {e}")
                return
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya çözülemedi: {e}")
    
    def sifre_hesapla(self, element, derece, sayi):
        """Verilen parametrelere göre şifreyi hesaplar"""
        try:
            # Dereceye göre hesaplama
            if derece == 30:
                cikarilacak = 12
                artis = 1
            elif derece == 60:
                cikarilacak = 24
                artis = 2
            elif derece == 90:
                cikarilacak = 36
                artis = 3
            elif derece == 120:
                cikarilacak = 48
                artis = 4
            elif derece == 150:
                cikarilacak = 60
                artis = 5
            else:  # 180
                cikarilacak = 72
                artis = 6
                
            hesaplanan = sayi - cikarilacak
            if hesaplanan < 0:
                QMessageBox.warning(self, "Uyarı", f"Sayı ({sayi}) {cikarilacak} değerinden küçük olmamalı!")
                return None
                
            bolum = hesaplanan // 3
            kalan = hesaplanan % 3
            
            # 9 sayı hesaplama
            sayilar = []
            for i in range(9):
                if i == 0:
                    sayilar.append(bolum)
                elif i == 6 and kalan > 0:  # 7. sayı (0-indeksli 6) kalan eklenir
                    sayilar.append(bolum + (i * artis) + kalan)
                else:
                    sayilar.append(bolum + (i * artis))
            
            # Elemente göre sıralama
            sifreli_sayilar = []
            ebced_değerleri = []  # Ebced değerlerini saklayacak liste
            
            if element == "Toprak":
                siralama = [1, 8, 3, 0, 4, 5, 7, 6, 2]  # 2,9,4,1,5,6,8,7,3
            elif element == "Ateş":
                siralama = [3, 2, 7, 8, 4, 0, 1, 6, 5]  # 4,3,8,9,5,1,2,7,6
            elif element == "Hava":
                siralama = [7, 0, 5, 2, 4, 6, 3, 8, 1]  # 8,1,6,3,5,7,4,9,2
            else:  # Su
                siralama = [5, 6, 1, 0, 4, 8, 7, 2, 3]  # 6,7,2,1,5,9,8,3,4
                
            for idx in siralama:
                if idx < len(sayilar):
                    sifreli_sayilar.append(str(sayilar[idx]))
                    ebced_değerleri.append(sayilar[idx])  # Ebced dönüşümü için sayıları kaydet
            
            # Sayısal şifre
            sifre = ''.join(sifreli_sayilar)
            
            # Ebced şifresi
            ebced_sifre = ""
            for i, deger in enumerate(ebced_değerleri):
                ebced_metin = self.sayi_ebced_donusumu(deger)
                ebced_sifre += str(deger) + ebced_metin
            
            # WinRAR için şifreyi düzenle - sadece alfanumerik ve sayılar kalsın
            rar_sifre = ''.join(karakter for karakter in ebced_sifre if karakter.isalnum())
            if not rar_sifre:
                rar_sifre = sifre  # Boşsa orijinal sayısal şifreyi kullan
            
            return rar_sifre
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Şifre hesaplanamadı: {e}")
            return None
            
    def metni_tersine_cevir(self, metin, satir_sayisi):
        """Şifrelenmiş metni orijinal haline çevirir, satır sayısına göre"""
        try:
            # Metin çok kısaysa
            if len(metin) < 2:
                return metin
            
            # Adım 1: Metni satırlara böl
            satirlar = self.metni_satirlara_bol(metin, satir_sayisi)
            
            # Adım 2: Her satırı ayrı ayrı ter çevir (bir son bir baş işleminin tersi)
            ara_satirlar = []
            for satir in satirlar:
                ara_satirlar.append(self.bir_son_bir_bas_tersi(satir))
                
            # Adım 3: Ara sonucu birleştir
            ara_sonuc = ''.join(ara_satirlar)
            
            # Adım 4: Tüm metni tekrar ter çevirme (bir son bir baş işleminin tersi)
            sonuc = self.bir_son_bir_bas_tersi(ara_sonuc)
            
            return sonuc
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Metin düzeltme hatası: {e}")
            return metin
    
    def bir_son_bir_bas_tersi(self, metin):
        """Bir son bir baş işlemini tersine çevirir"""
        if len(metin) <= 1:
            return metin
            
        # Sonuç metnini oluştur
        sonuc = [''] * len(metin)
        
        # Bir son bir baş şeklinde olan metni tekrar aslına çevir
        for i in range(0, len(metin), 2):
            # Çift indeksler = son karakterler
            if i < len(metin):
                # Sondaki karakter
                sonuc[len(metin) - 1 - (i // 2)] = metin[i]
            
            # Tek indeksler = baş karakterler
            if i + 1 < len(metin):
                sonuc[i // 2] = metin[i + 1]
            
        # Tek sayıda karakter varsa, ortadaki karakteri ayarla
        if len(metin) % 2 == 1:
            orta_index = len(metin) // 2
            sonuc[orta_index] = metin[len(metin) - 1]
        
        return ''.join(sonuc)

    def ebced_hesapla(self, rakam):
        """Ebced değerlerini hesaplayan fonksiyon"""
        rakam_map = {
            1: "â",
            2: "Be",
            3: "Cim",
            4: "Dal",
            5: "He",
            6: "Vav",
            7: "Ze",
            8: "Ha",
            9: "Tı",
            10: "Ye",
            20: "Kef",
            30: "Lam",
            40: "Mim",
            50: "Nun",
            60: "Sin",
            70: "Ayn",
            80: "Fe",
            90: "Sad",
            100: "Kaf",
            200: "Re",
            300: "Sin",
            400: "Te",
            500: "Se",
            600: "Hı",
            700: "Zel",
            800: "Dad",
            900: "Zı",
            1000: "Ğayın"
        }
        
        return rakam_map.get(rakam, "")
    
    def ucbasamak(self, metin, ekle_ve=True):
        """Metne 've' veya 'in' ekler"""
        if not metin:
            return ""
        if ekle_ve:
            return f"{metin} ve "
        return f"{metin} "
    
    def sayi_ebced_donusumu(self, deger):
        """Sayıyı Ebced değerlerine dönüştürür ve uygun formatı oluşturur"""
        sonuc = ""
        
        if deger < 100:
            birler = deger % 10
            onlar = (deger % 100) - birler
            sonuc = f"{self.ucbasamak(self.ebced_hesapla(onlar), True)}{self.ucbasamak(self.ebced_hesapla(birler), False)}in"
        elif deger < 1000:
            birler = deger % 10
            onlar = (deger % 100) - birler
            yuzler = (deger % 1000) - (birler + onlar)
            sonuc = f"{self.ucbasamak(self.ebced_hesapla(yuzler), True)}{self.ucbasamak(self.ebced_hesapla(onlar), True)}{self.ucbasamak(self.ebced_hesapla(birler), False)}in"
        elif deger >= 1000 and deger < 2000:
            birler = deger % 10
            onlar = (deger % 100) - birler
            yuzler = (deger % 1000) - (birler + onlar)
            sonuc = f"{self.ucbasamak(self.ebced_hesapla(1000), True)}{self.ucbasamak(self.ebced_hesapla(yuzler), True)}{self.ucbasamak(self.ebced_hesapla(onlar), True)}{self.ucbasamak(self.ebced_hesapla(birler), False)}in"
        elif deger >= 2000 and deger < 10000:
            birler = deger % 10
            onlar = (deger % 100) - birler
            yuzler = (deger % 1000) - (birler + onlar)
            binler = ((deger % 10000) - (yuzler + onlar + birler)) // 1000
            sonuc = f"{self.ucbasamak(self.ebced_hesapla(binler), True)}{self.ucbasamak(self.ebced_hesapla(1000), True)}{self.ucbasamak(self.ebced_hesapla(yuzler), True)}{self.ucbasamak(self.ebced_hesapla(onlar), True)}{self.ucbasamak(self.ebced_hesapla(birler), False)}in"
        elif deger >= 10000 and deger < 100000:
            birler = deger % 10
            onlar = (deger % 100) - birler
            yuzler = (deger % 1000) - (birler + onlar)
            binler = ((deger % 10000) - (yuzler + onlar + birler)) // 1000
            onbinler = ((deger % 100000) - (deger % 10000)) // 10000
            sonuc = f"{self.ucbasamak(self.ebced_hesapla(onbinler), True)}{self.ucbasamak(self.ebced_hesapla(binler), True)}{self.ucbasamak(self.ebced_hesapla(1000), True)}{self.ucbasamak(self.ebced_hesapla(yuzler), True)}{self.ucbasamak(self.ebced_hesapla(onlar), True)}{self.ucbasamak(self.ebced_hesapla(birler), False)}in"
        else:
            birler = deger % 10
            onlar = (deger % 100) - birler
            yuzler = (deger % 1000) - (birler + onlar)
            binler = ((deger % 10000) - (yuzler + onlar + birler)) // 1000
            onbinler = ((deger % 100000) - (deger % 10000)) // 10000
            yuzbinler = ((deger % 1000000) - (deger % 100000)) // 100000
            sonuc = f"{self.ucbasamak(self.ebced_hesapla(yuzbinler), True)}{self.ucbasamak(self.ebced_hesapla(onbinler), True)}{self.ucbasamak(self.ebced_hesapla(binler), False)}{self.ucbasamak(self.ebced_hesapla(1000), True)}{self.ucbasamak(self.ebced_hesapla(yuzler), True)}{self.ucbasamak(self.ebced_hesapla(onlar), True)}{self.ucbasamak(self.ebced_hesapla(birler), False)}in"
        
        return sonuc

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SifrelemeFormu()
    window.show()
    sys.exit(app.exec_()) 