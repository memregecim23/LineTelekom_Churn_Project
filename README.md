<img width="1272" height="759" alt="image" src="https://github.com/user-attachments/assets/8267207a-611c-4159-b51c-40ad749a6cd2" />
<img width="1076" height="785" alt="image" src="https://github.com/user-attachments/assets/add972c2-e9e8-4c1e-ab7c-09c7465d9f96" />



Not:Aşağıdaki linke tıklayarak canlı olarak demoyu deneyebilirsiniz.Link aynı zamanda about kısmında da bulunmaktadır.
https://linetelekomchurnprojects.streamlit.app/

# Telco Customer Churn Prediction System

Bu proje, bir telekomünikasyon şirketinin müşteri verilerini analiz ederek, hangi müşterilerin hizmeti bırakma (**Churn**) ihtimali olduğunu tahmin eden bir makine öğrenmesi uygulamasıdır.

## Veri Seti Hikayesi ve Değişkenler

Proje, **7043** müşteriye ait demografik bilgileri, hizmet kullanım detaylarını ve fatura bilgilerini içeren *Telco Customer Churn* veri setini kullanır.  
Hedef değişkenimiz **Churn** (Müşterinin ayrılıp ayrılmadığı) sütunudur.

### Değişken Tablosu

| Değişken Adı | Açıklama |
| :--- | :--- |
| **customerID** | Müşteriye özel benzersiz kimlik numarası (Modelde kullanılmaz). |
| **gender** | Müşterinin cinsiyeti (Male/Female). |
| **SeniorCitizen** | Müşterinin yaşlı vatandaş olup olmadığı (1: Evet, 0: Hayır). |
| **Partner** | Müşterinin bir ortağı/eşi olup olmadığı (Yes/No). |
| **Dependents** | Müşterinin bakmakla yükümlü olduğu kişiler var mı? (Yes/No). |
| **tenure** | Müşterinin şirkette kaldığı ay sayısı (Müşteri ömrü). |
| **PhoneService** | Telefon hizmeti alıp almadığı. |
| **MultipleLines** | Birden fazla hattı olup olmadığı. |
| **InternetService** | İnternet servis sağlayıcısı (DSL, Fiber optic, No). |
| **OnlineSecurity** | Online güvenlik hizmeti var mı? |
| **OnlineBackup** | Online yedekleme hizmeti var mı? |
| **DeviceProtection** | Cihaz koruma sigortası var mı? |
| **TechSupport** | Teknik destek alıyor mu? |
| **StreamingTV** | TV yayın hizmeti var mı? |
| **StreamingMovies** | Film izleme hizmeti var mı? |
| **Contract** | Sözleşme türü (Month-to-month, One year, Two year). |
| **PaperlessBilling** | Kağıtsız fatura kullanıyor mu? |
| **PaymentMethod** | Ödeme yöntemi (Electronic check, Mailed check, Bank transfer, Credit card). |
| **MonthlyCharges** | Müşteriden aylık tahsil edilen tutar. |
| **TotalCharges** | Müşteriden o güne kadar tahsil edilen toplam tutar. |
| **Churn** | **HEDEF DEĞİŞKEN:** Müşteri ayrıldı mı? (Yes/No). |

## Model Performansı

Bu projede güçlü ve hızlı bir sınıflandırma algoritması olan **XGBoost** kullanılmıştır.

* **Kullanılan Algoritma:** `XGBClassifier`
### Model Performans Sonuçları

#### 1. Confusion Matrix (Karmaşıklık Matrisi)
| Gerçek \ Tahmin | 0 (Negatif) | 1 (Pozitif) |
| :--- | :---: | :---: |
| **0** | 1089 | 186 |
| **1** | 260 | 1015 |

#### 2. Sınıflandırma Raporu (Classification Report)
| Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **0** | 0.81 | 0.85 | 0.83 | 1275 |
| **1** | 0.85 | 0.80 | 0.82 | 1275 |
| **Accuracy** | | | **0.83** | **2550** |
| **Macro Avg** | 0.83 | 0.83 | 0.82 | 2550 |
| **Weighted Avg**| 0.83 | 0.83 | 0.82 | 2550 |

**Genel Doğruluk (Exact Accuracy):** `%82.51` (0.825098)

**Kurulum ve Çalıştırma**

1.Gerekli Kütüphaneleri Yükleyin
**pip install -r requirements.txt**

2.baslat.py dosyasındaki main'i run ederek uygulamayı başlatın

**(Not:Klasör ve dosya yapısı repodaki gibi olmalıdır.)**

Geliştirici: Mustafa Emre Geçim



















































