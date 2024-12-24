# Place_Analysis
Bu proje, kullanıcılara mekan önerilerinde bulunmak için K-Nearest Neighbors (KNN) algoritmasını kullanan bir Streamlit uygulamasıdır. Kullanıcılar fiyat, konum, etkinlik türü gibi kriterler doğrultusunda öneriler alabilir ve KNN algoritması sayesinde puanladıkları mekanlara benzer mekanlar önerilir.
Mekan Öneri Uygulaması

Bu proje, kullanıcılara mekan önerilerinde bulunmak için K-Nearest Neighbors (KNN) algoritmasını kullanan bir Streamlit uygulamasıdır. Kullanıcılar fiyat, konum, etkinlik türü gibi kriterler doğrultusunda öneriler alabilir ve KNN algoritması sayesinde puanladıkları mekanlara benzer mekanlar önerilir.

Proje Özellikleri

1. Mekan Öneri

Kullanıcılar etkinlik türü, lokasyon ve fiyat aralığı seçerek mekan önerileri alabilir.

Mekanlar, kullanıcı puanlarına göre sıralanır.

2. Mekan Ekleme

Kullanıcılar yeni mekanlar ekleyebilir.

Eklenen mekanlar mevcut veri setine dahil edilir ve önerilerde kullanılabilir.

3. Puanlama Analizi

Kullanıcılar mekanlara puan verebilir.

Mekanların ortalama puanları görüntülenebilir.

4. Mekan Seçenekleri (KNN Önerisi)

Kullanıcının yüksek puanladığı mekanlara benzer mekanlar önerilir.

Öneriler "Cuisine Type", "Price Range", ve "Location" bilgileriyle birlikte gösterilir.

Kurulum

Gereksinimler

Python 3.8 veya üzeri

Gereken Python kütüphaneleri:

streamlit

pandas

scikit-learn

numpy

Adımlar

Bu repoyu klonlayın:

git clone https://github.com/kullaniciadi/mekan-oneri.git
cd mekan-oneri

Gerekli kütüphaneleri yükleyin:

pip install -r requirements.txt

Uygulamayı çalıştırın:

streamlit run app.py

Uygulamayı kullanın:
Tarayıcınızda http://localhost:8501 adresine giderek uygulamayı görüntüleyebilirsiniz.

Kullanım

Mekan Öneri

Etkinlik türünü, konumu ve fiyat aralığını seçin.

Uygulama, kriterlerinize uygun mekanları listeler.

En yüksek puanlı mekanlar ayrıca vurgulanır.

Mekan Ekleme

Yeni bir mekan eklemek için gerekli bilgileri doldurun (isim, mutfak türü, fiyat aralığı, vb.).

Eklediğiniz mekanlar öneri sistemine dahil edilir.

Puanlama Analizi

Mekanlara puan vererek öneri algoritmasını zenginleştirin.

Tüm mekanların ortalama puanlarını görüntüleyin.

Mekan Seçenekleri (KNN Önerisi)

Kullanıcı ID'nizi girerek size önerilen mekanları görüntüleyin.

Öneriler, "Cuisine Type", "Price Range", ve "Location" bilgilerini içerir.

Veri Seti

Proje, bir CSV dosyası (PlacesAnalysis.csv) kullanır. Bu dosya şu başlıkları içerir:

Place Name: Mekan adı

Cuisine Type: Mutfak türü

Price Range: Fiyat aralığı

Price Range Unit: Sayısal fiyat bilgisi

Event Type: Etkinlik türü

Location: Mekanın bulunduğu yer

User Rating (1-5): Kullanıcı puanı

Örnek Veri:

Place Name

Cuisine Type

Price Range

Price Range Unit

Event Type

Location

User Rating (1-5)

Cafe Aroma

Coffee

$$

2

Casual

Downtown

4.2

Bistro Delight

Italian

$$$

3

Formal

Midtown

4.8

Teknik Detaylar

KNN Algoritması

Kullanıcının yüksek puanladığı mekanlara benzer mekanlar önerilir.

Euclidean Distance metriği kullanılarak benzerlik hesaplanır.

Kategorik özellikler (Cuisine Type, Location) one-hot encoding ile sayısallaştırılır.

Eksik sütunlar doldurularak modelin uyumlu çalışması sağlanır.

Katkı

Hataları bildirmek veya geliştirme önerilerinde bulunmak için bir issue açabilirsiniz.

Katkılarınızı pull request ile sunabilirsiniz.

Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakabilirsiniz.
