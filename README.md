<img width="1218" height="798" alt="image" src="https://github.com/user-attachments/assets/a08fe0d0-25b2-4451-9691-1d1caa8b8130" />
<img width="1282" height="831" alt="image" src="https://github.com/user-attachments/assets/491d6b97-9c5c-409e-966c-2cc2e7279e16" />

Not:Aşağıdaki linke tıklayarak canlı olarak demoyu deneyebilirsiniz.Link aynı zamanda about kısmında da bulunmaktadır.
https://linetelekomchurnproject.streamlit.app/

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
Confusion Matrix:
[[923 352]
 [103 383]]

Classification Report:
              precision    recall  f1-score   support

           0       0.90      0.72      0.80      1275
           1       0.52      0.79      0.63       486

    accuracy                           0.74      1761
   macro avg       0.71      0.76      0.71      1761
weighted avg       0.80      0.74      0.75      1761

Accuracy Score: 0.7416
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



















































