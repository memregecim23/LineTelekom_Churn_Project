**Telco Customer Churn Prediction System**
Bu proje, bir telekomünikasyon şirketinin müşteri verilerini analiz ederek, hangi müşterilerin hizmeti bırakma (Churn) ihtimali olduğunu tahmin eden bir makine öğrenmesi uygulamasıdır.

**Veri Seti Hikayesi ve Değişkenler**
Proje, 7043 müşteriye ait demografik bilgileri, hizmet kullanım detaylarını ve fatura bilgilerini içeren Telco Customer Churn veri setini kullanır. 
Hedef değişkenimiz Churn (Müşterinin ayrılıp ayrılmadığı) sütunudur.

**Değişken Adı,Açıklama**
customerID,Müşteriye özel benzersiz kimlik numarası (Modelde kullanılmaz).
gender,Müşterinin cinsiyeti (Male/Female).
SeniorCitizen,"Müşterinin yaşlı vatandaş olup olmadığı (1: Evet, 0: Hayır)."
Partner,Müşterinin bir ortağı/eşi olup olmadığı (Yes/No).
Dependents,Müşterinin bakmakla yükümlü olduğu kişiler var mı? (Yes/No).
tenure,Müşterinin şirkette kaldığı ay sayısı (Müşteri ömrü).
PhoneService,Telefon hizmeti alıp almadığı.
MultipleLines,Birden fazla hattı olup olmadığı.
InternetService,"İnternet servis sağlayıcısı (DSL, Fiber optic, No)."
OnlineSecurity,Online güvenlik hizmeti var mı?
OnlineBackup,Online yedekleme hizmeti var mı?
DeviceProtection,Cihaz koruma sigortası var mı?
TechSupport,Teknik destek alıyor mu?
StreamingTV,TV yayın hizmeti var mı?
StreamingMovies,Film izleme hizmeti var mı?
Contract,"Sözleşme türü (Month-to-month, One year, Two year)."
PaperlessBilling,Kağıtsız fatura kullanıyor mu?
PaymentMethod,"Ödeme yöntemi (Electronic check, Mailed check, Bank transfer, Credit card)."
MonthlyCharges,Müşteriden aylık tahsil edilen tutar.
TotalCharges,Müşteriden o güne kadar tahsil edilen toplam tutar.
Churn,HEDEF DEĞİŞKEN: Müşteri ayrıldı mı? (Yes/No).

**Model Performansı**
Bu projede Support Vector Classifier (SVC) algoritması kullanılmıştır. 
Dengesiz veri setini yönetmek için class_weight="balanced" parametresi ve Probability Threshold = 0.25 (Hassas Tahmin) ayarı tercih edilmiştir.

- Algoritma: SVC (Kernel: RBF)
- Doğruluk (Accuracy): ~%75.4
- Özellik: Model, müşteri kaybını (Churn) kaçırmamak için hassas ayarlanmıştır.

**Kurulum ve Çalıştırma**

1.Gerekli Kütüphaneleri Yükleyin
**pip install -r requirements.txt**

2.Uygulamayı Başlatın
- Proje klasörüne gidin.
- Klasör içindeki boş bir alana Sağ Tık yapın.
- "Open in Terminal" (veya Git Bash Here) seçeneğine tıklayın.
- Açılan siyah ekrana şu komutu yazıp Enter'a basın:
**streamlit run app.py**

**(Not: Eğer dosya adınız farklıysa app.py yerine kendi dosya adınızı yazınız.)**

Geliştirici: Mustafa Emre Geçim



















































