# Şifreleme Uygulaması

Bu uygulama, metinleri BAST ve Ebced şifreleme sistemleri kullanarak şifrelemek ve çözmek için tasarlanmış bir Python aracıdır.

## Özellikler

- **Metin Şifreleme**: Metinleri özel algoritma ile şifreler
- **Şifreli RAR Oluşturma**: Şifrelenen metinleri şifreli RAR dosyalarına dönüştürür
- **Otomatik Çözümleme**: Şifreli dosyaları parametre bilgilerine göre otomatik çözer
- **Element, Derece ve Satır Ayarları**: Şifreleme parametrelerini özelleştirme imkanı
- **BAST ve Ebced Dönüşümleri**: Geleneksel şifreleme sistemlerini kullanma
- **Çift Katmanlı Şifreleme**: Hem metin algoritması hem de BAST/Ebced sistemi ile şifreleme
- **Otomatik Dosya Adı Formatı**: Çözüm için gerekli tüm bilgileri içeren dosya adı oluşturma
- **Base64 Kodlama**: Metin verileri için ek güvenlik katmanı
- **WinRAR Entegrasyonu**: Şifreli arşiv dosyaları oluşturma ve çözme

## Kurulum

Uygulamayı kullanmak için aşağıdaki adımları izleyin:

1. Python 3.6 veya üzeri sürümü yükleyin
2. Gerekli bağımlılıkları yükleyin:

```
pip install PyQt5==5.15.9
```

3. WinRAR programının kurulu olduğundan emin olun (varsayılan kurulum dizinleri kontrol edilir)
4. Uygulamayı çalıştırın:

```
python SifrelemeHVS.py
```

## Kullanım

### Şifreleme Sekmesi

1. **Element**: Ateş, Su, Toprak veya Hava elementlerinden birini seçin (şifreleme algoritmasında farklı sayı sıralamaları kullanılır)
2. **Derece**: 30, 60, 90, 120, veya 180 derece seçin (hesaplama formülünde çıkarılacak değeri ve artış değerini etkiler)
3. **Satır Sayısı**: 1-7 arası bir değer seçin (metin karıştırma algoritmasında satır sayısını belirler)
4. **Başlık**: Dosya adında görünecek başlık metni (RAR dosyası içindeki metin dosyasının da adı olur)
5. **Sayı**: Temel şifreleme sayısı (bu sayıdan dereceye göre belirlenen değer çıkarılır ve algoritma başlatılır)
6. **Metin**: Şifrelenecek metin girin
7. **Metni Dönüştür**: Metni şifreleme algoritmasıyla karıştırır (bir son bir baş algoritması)
8. **Şifrele**: RAR şifresi oluşturur, metni Base64 ile kodlar ve şifreli RAR dosyası oluşturur

### Çözme Sekmesi

1. **Dosya Seç**: Şifreli RAR dosyasını seçin (dosya adı otomatik olarak analiz edilir)
2. **Çözümle**: Dosya adından parametreleri çıkarır, doğru şifreyi hesaplar, RAR dosyasını açar ve şifrelenmiş metni çözümler

## Teknik Detaylar

### Şifreleme Algoritması

1. **Metin Dönüştürme**: `bir_son_bir_bas()` metodu ile metni karıştırır
   - Metindeki karakterler sondan ve baştan sırayla alınarak yeni metin oluşturulur
   - Örnek: "ABCDEF" → "FAEBDC" (F + A + E + B + D + C)
   
2. **Satır Bölme**: Metni seçilen sayıda satıra böler
   - Metin eşit uzunlukta satırlara bölünür
   - Her satır bağımsız olarak işlenir
   - Satır uzunluğu = Toplam karakter / Satır sayısı (yukarı yuvarlanır)
   
3. **Satır İşleme**: Her satırı ayrı ayrı işler ve karıştırır
   - Her satır kendi içinde `bir_son_bir_bas()` algoritmasıyla karıştırılır
   - Karıştırılmış satırlar birleştirilir
   
4. **Base64 Şifreleme**: Şifrelenmiş metin Base64 formatına dönüştürülür
   - Metne şifreleme metadata bilgileri eklenir (SATIR, ELEMENT, DERECE, SAYI, BAST_DEGER vb.)
   - UTF-8 kodlamasıyla binary formata dönüştürülür ve Base64 ile kodlanır
   
5. **RAR Şifreleme**: WinRAR kullanılarak şifreli RAR oluşturulur
   - Şifre, algoritma ile hesaplanan Ebced değerlerinden oluşturulur
   - Geçici klasöre önce şifrelenmiş metin dosyası kaydedilir
   - WinRAR komutu çalıştırılarak şifreli arşiv oluşturulur
   - İşlem sonunda geçici dosyalar temizlenir

### Şifre Hesaplama Mantığı

1. **Temel Hesaplama**:
   - Girilen sayıdan dereceye göre belirlenen değer çıkarılır (30° → 12, 60° → 24, 90° → 36, 120° → 48, 180° → 72)
   - Sonuç 3'e bölünür (bölüm ve kalan hesaplanır)
   - Bölüm değeri taban olarak kullanılır
   - 9 sayı oluşturulur:
     * İlk sayı: bölüm
     * Diğer sayılar: bölüm + (sıra * artış) [artış değeri dereceye göre değişir: 30° → 1, 60° → 2, 90° → 3, 120° → 4, 180° → 6]
     * 7. sayıya (0-indeksli 6) kalan eklenir

2. **Element İşleme**:
   - Elementin türüne göre 9 sayı farklı bir sıralamaya göre dizilir:
     * Toprak: [1,8,3,0,4,5,7,6,2] indeks sıralaması (2,9,4,1,5,6,8,7,3 sayı sıralaması)
     * Ateş: [3,2,7,8,4,0,1,6,5] indeks sıralaması (4,3,8,9,5,1,2,7,6 sayı sıralaması)
     * Hava: [7,0,5,2,4,6,3,8,1] indeks sıralaması (8,1,6,3,5,7,4,9,2 sayı sıralaması)
     * Su: [5,6,1,0,4,8,7,2,3] indeks sıralaması (6,7,2,1,5,9,8,3,4 sayı sıralaması)

3. **Ebced ve BAST Dönüşümü**:
   - Her sayı Ebced sisteminde harflere dönüştürülür
   - Ebced şifresi: Her sayı + karşılık gelen Ebced değeri birleştirilir
   - BAST değeri: Sayının her basamağı BAST tablosuna göre kodlanır

### BAST Sistemi (Detaylı)

BAST şifreleme, sayı değerlerini özel kodlara dönüştüren bir sistemdir. İki farklı tablo kullanılır:

1. **BAST 4 Tablosu**: Birler basamağı çift (2,4,6,8) olan veya onlar basamağı çift (20,40,60,80) olan sayılar için kullanılır
   - Örnek değerler: 1→1641, 2→1046, 3→451, 4→1995, 5→1783, 6→1832, 7→1980, 8→1288, 9→1616
   - Onlar: 10→2243, 20→1968, 30→1086, 40→2439, 50→1843, 60→1748, 70→1997, 80→1843, 90→2513
   - Yüzler: 100→1309, 200→2447, 300→1591, 400→3313, 500→2793, 600→2088, 700→1777, 800→506, 900→2627
   - Binler: 1000→1391

2. **BAST 5 Tablosu**: Birler basamağı tek (1,3,5,7,9) olan veya onlar basamağı tek (10,30,50,70,90) olan sayılar için kullanılır
   - Örnek değerler: 1→991, 2→921, 3→1118, 4→2011, 5→2007, 6→2482, 7→1364, 8→1889, 9→1683
   - Onlar: 10→2616, 20→1842, 30→1239, 40→2703, 50→2149, 60→1260, 70→1443, 80→2148, 90→3113
   - Yüzler: 100→1749, 200→1547, 300→1488, 400→3870, 500→2561, 600→1999, 700→647, 800→1231, 900→2028
   - Binler: 1000→1820

3. **BAST Dönüşümü Algoritması**:
   - Sayının basamaklarına ayrılır (birler, onlar, yüzler, binler...)
   - Her basamak için çift/tek kontrolü yapılır
   - Uygun BAST tablosundan değer alınır
   - Değerler tire (-) ile birleştirilir
   - Örnek: 123 sayısı için → "1749-1968-1118"

### Ebced Sistemi (Detaylı)

Ebced, Arap alfabesindeki harflere sayısal değerler atayan geleneksel bir sistemdir:

1. **Temel Ebced Değerleri**:
   - â (1), Be (2), Cim (3), Dal (4), He (5), Vav (6), Ze (7), Ha (8), Tı (9)
   - Ye (10), Kef (20), Lam (30), Mim (40), Nun (50), Sin (60), Ayn (70), Fe (80), Sad (90)
   - Kaf (100), Re (200), Sin (300), Te (400), Se (500), Hı (600), Zel (700), Dad (800), Zı (900), Ğayın (1000)

2. **Ebced Metni Oluşturma**:
   - Sayı basamaklarına ayrılır
   - Her basamak değeri için Ebced karşılığı bulunur
   - Basamak değerleri "ve" bağlacı ile birleştirilir
   - Sonuna "in" eklenir
   - Örnek: 23 → "Kef ve Cim in" (20 ve 3 in)

3. **RAR Şifresi Oluşturma**:
   - Her sayı ve Ebced metni birleştirilir
   - Alfanumerik olmayan karakterler kaldırılır
   - Örnek: 123 → "100Kaf ve 20Kef ve 3Cim in" → "100Kaf20Kef3Cimin"

### Dosya Adı Formatı (Detaylı)

```
[SatırSayısı][ElementHarf][Derece],[Sayı],[BAST],[SatırSayısı]_[Başlık].rar
```

Dosya adı, çözümleme için gereken tüm parametreleri içerir:

1. **SatırSayısı**: Metni kaç satıra böldüğümüz (1-7 arası)
2. **ElementHarf**: Element türünün ilk harfi (A: Ateş, S: Su, T: Toprak, H: Hava)
3. **Derece**: Şifreleme derecesi (30, 60, 90, 120, 180)
4. **Sayı**: Temel şifreleme sayısı
5. **BAST**: Sayının BAST kodlaması
6. **SatırSayısı**: Yeniden satır sayısı (tutarlılık kontrolü için)
7. **Başlık**: Kullanıcının girdiği başlık

Örnek: `3T90,144,991-1239,3_TestDosyasi.rar`
- 3 satır
- Toprak elementi
- 90 derece
- 144 sayısı
- BAST değeri: 991-1239
- 3 satır (tutarlılık kontrolü)
- Başlık: TestDosyasi

### Metin Çözme Algoritması (Detaylı)

1. **Dosya Bilgilerini Çıkarma**:
   - Dosya adından satır sayısı, element, derece ve sayı değerleri çıkarılır
   - Bu parametreler kullanılarak şifre hesaplanır

2. **RAR Açma**:
   - Hesaplanan şifre ile WinRAR kullanılarak dosya geçici klasöre çıkarılır

3. **Metin Çözme**:
   - Base64 ile kodlanmış metin çözülür
   - Metadata bilgileri ayrıştırılır (SATIR, ELEMENT, DERECE, SAYI vb.)
   - Şifrelenmiş metin çözme algoritmasına verilir

4. **Ters Şifreleme Algoritması**:
   - `metni_tersine_cevir()` fonksiyonu kullanılır:
     1. Metin, dosya adından veya metadata'dan alınan satır sayısına göre satırlara bölünür
     2. Her satır `bir_son_bir_bas_tersi()` metoduyla çözülür
     3. Çözülen satırlar birleştirilir
     4. Sonuç metni tekrar `bir_son_bir_bas_tersi()` ile işlenir
     5. Orijinal metin elde edilir

5. **bir_son_bir_bas_tersi()** (Detaylı):
   - Bu fonksiyon, "bir son bir baş" algoritmasını tersine çevirir
   - Şifrelenmiş metindeki karakterleri doğru konumlara geri yerleştirir
   - Tek ve çift indeksli karakterler ayrı ayrı işlenir
   - Çift indeksli karakterler: Metni sondan başa doğru yerleştirir
   - Tek indeksli karakterler: Metni baştan sona doğru yerleştirir

## Hata Ayıklama ve Güvenlik

### Hata Tespiti ve Güvenlik Kontrolleri

1. **WinRAR Kontrolü**: 
   - Uygulama başlangıcında WinRAR uygulamasının varlığı kontrol edilir
   - Alternatif kurulum dizinleri otomatik olarak kontrol edilir
   - Bulunamazsa kullanıcıya uyarı verilir

2. **Dosya Adı Kontrolü**:
   - Dosya adı formatının doğruluğu kontrol edilir
   - Satır sayısı tutarlılığı kontrol edilir
   - Element harfinin geçerliliği kontrol edilir

3. **Şifreleme Parametreleri**:
   - Tüm alanların doldurulması kontrol edilir
   - Sayısal değerlerin geçerliliği kontrol edilir
   - Hesaplanan değerlerin sınırlar içinde olması kontrol edilir

4. **Geçici Dosya Yönetimi**:
   - İşlemler için geçici dizin oluşturulur
   - Her işlem öncesi geçici dosyalar temizlenir
   - İşlem sonunda geçici dosyalar otomatik olarak silinir

### Debug Mesajları

Uygulama çalışırken detaylı debug mesajları konsola yazdırılır:

- Metin dönüştürme adımları
- BAST dönüşüm değerleri
- Dosya bilgisi çıkarma adımları
- RAR komut satırı
- Hata mesajları

Bu mesajlar, olası sorunların teşhisinde yardımcı olur.

## Lisans

Bu yazılım açık kaynak olarak MIT lisansı altında sunulmuştur.
