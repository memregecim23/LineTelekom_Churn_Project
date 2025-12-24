import numpy as np

# ---------------------------------------------------------
# NUMPY 2.0 UYUMLULUK YAMASI 
# ---------------------------------------------------------
# Scikit-learn ve SciPy eski sürümleri NumPy 2.0 ile çalışırken bu fonksiyonları arıyor.
try:
    # 'trapz' hatası için:
    if not hasattr(np, 'trapz'):
        np.trapz = np.trapezoid

    # 'in1d' hatası için:
    if not hasattr(np, 'in1d'):
        np.in1d = np.isin

    # 'float_' hatası için:
    if not hasattr(np, 'float_'):
        np.float_ = np.float64
except AttributeError:
    pass
# ---------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import os

# Sayfa Ayarları
st.set_page_config(
    page_title="LİNETELEKOM A.Ş CHURN ANALİZ SİSTEMİ",
    layout="centered"
)


try:
    os.listdir()
except:
    st.write("Dosya listesi okunamadı.")


# ---------------------------------------------------------
# MODEL EĞİTİM FONKSİYONU (YENİ KODLARINLA GÜNCELLENDİ)
# ---------------------------------------------------------
@st.cache_resource(show_spinner="Model eğitiliyor, lütfen bekleyin...")
def train_model_live():
    # Veri Yükleme
    try:
        dfChurn = pd.read_csv("Churn.csv")
    except FileNotFoundError:
        return None, None, "CSV"

    # --- VERİ ÖN İŞLEME (SENİN YENİ KODLARIN) ---

    # TotalCharges düzenleme
    dfChurn["TotalCharges"] = pd.to_numeric(dfChurn["TotalCharges"], errors='coerce')
    dfChurn["TotalCharges"] = dfChurn["TotalCharges"].fillna(2700.0)
    dfChurn["TotalCharges"] = dfChurn["TotalCharges"].astype(float)

    # Label Encoding (Manuel Mapping ile daha güvenli)
    binary_cols = ["Partner", "Dependents", "PhoneService", "PaperlessBilling", "Churn",
                   "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
                   "StreamingTV", "StreamingMovies"]

    for col in binary_cols:
        dfChurn[f"{col}_encode"] = dfChurn[col].apply(lambda x: 1 if x == "Yes" else 0)

    # Gender ve SeniorCitizen özel durum
    dfChurn["gender_encode"] = dfChurn["gender"].apply(lambda x: 1 if x == "Male" else 0)
    dfChurn["SeniorCitizen_encode"] = dfChurn["SeniorCitizen"]  # Zaten 0-1

    # MultipleLines (No phone service -> 0 kabul edelim basitlik için)
    dfChurn["MultipleLines_encode"] = dfChurn["MultipleLines"].apply(lambda x: 1 if x == "Yes" else 0)

    # Ordinal Encoding
    ordinal_internetservices = OrdinalEncoder(categories=[["No", "DSL", "Fiber optic"]])
    ordinal_contract = OrdinalEncoder(categories=[["Month-to-month", "One year", "Two year"]])

    dfChurn["InternetService_encode"] = ordinal_internetservices.fit_transform(dfChurn[["InternetService"]])
    dfChurn["Contract_encode"] = ordinal_contract.fit_transform(dfChurn[["Contract"]])

    # Tipleri int yapma
    dfChurn["InternetService_encode"] = dfChurn["InternetService_encode"].astype(int)
    dfChurn["Contract_encode"] = dfChurn["Contract_encode"].astype(int)

    # One-Hot Encoding (PaymentMethod)
    dfChurnencode = pd.get_dummies(dfChurn, columns=["PaymentMethod"])

    # Gereksiz Sütunları Düşürme (String olanlar)
    drop_cols_origin = ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
                        "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
                        "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
                        "StreamingMovies", "Contract", "PaperlessBilling", "Churn"]

    dfChurnencode.drop([c for c in drop_cols_origin if c in dfChurnencode.columns], axis=1, inplace=True)

    # --- DÜŞÜK KORELASYONLU SÜTUNLARI ÇIKARMA (SENİN ANALİZİN) ---
    low_corr = [
        "gender_encode",
        "PhoneService_encode",
        "StreamingTV_encode",
        "StreamingMovies_encode",
        "MultipleLines_encode"
    ]
    # Sadece var olanları düşür (Hata önlemek için)
    cols_to_drop = [c for c in low_corr if c in dfChurnencode.columns]
    dfChurnencode.drop(columns=cols_to_drop, axis=1, inplace=True)

    # X ve y ayrımı
    X = dfChurnencode.drop(["Churn_encode"], axis=1)
    y = dfChurnencode["Churn_encode"]

    # Eğitim seti ayırma
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=15)

    # SMOTE Uygulama (Veri Dengeleme)
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    # XGBoost Modeli Eğitimi
    # (GridSearch canlı sistemde çok yavaşlatır, o yüzden standart parametrelerini kullandım)
    xgb = XGBClassifier(n_estimators=100, random_state=42)
    xgb.fit(X_train_smote, y_train_smote)

    return xgb, X.columns, "OK"


# Fonksiyonu çalıştır
model_results = train_model_live()

# Hata Kontrolü
if model_results[2] == "CSV":
    st.error("🚨 HATA: 'Churn.csv' dosyası bulunamadı!")
    st.warning("Lütfen CSV dosyasını bu python dosyasının olduğu klasöre atın.")
    st.stop()
else:
    model, model_columns, status = model_results

# ---------------------------------------------------------
# STREAMLIT ARAYÜZÜ (ORİJİNAL TASARIM KORUNDU)
# ---------------------------------------------------------
st.title("📉 LİNETELEKOM İŞTE-İŞ CHURN ANALİZ UYGULAMASI")

with st.form("churn_form"):
    st.header("Müşteri Bilgileri")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hizmet & Sözleşme")
        tenure = st.number_input("Müşteri Süresi(AY)", min_value=0, value=12)
        monthly_charges = st.number_input("Aylık Ücret(küsüratlı giriniz)", min_value=0.0, value=220.5)
        total_charges = st.number_input("Toplam Ücret(küsüratlı giriniz)", min_value=0.0, value=1700.5)

        contract = st.selectbox("Sözleşme Türü", ["aydan-aya", "12 ay taahhüt", "24 ay taahhüt"])
        internet_service = st.selectbox("İnternet Servisi", ["Yok", "DSL", "Fiber optic"])

    with col2:
        st.subheader("Kişisel & Fatura")
        senior_citizen = st.selectbox("Yaşlı Vatandaş mı?", ["Hayır", "Evet"])
        partner = st.selectbox("Partneri Var mı?", ["Hayır", "Evet"])
        dependents = st.selectbox("Bakmakla Yükümlü?", ["Hayır", "Evet"])
        paperless_billing = st.selectbox("Kağıtsız Fatura?", ["Hayır", "Evet"])
        payment_method = st.selectbox("Ödeme Yöntemi", [
            "Electronic check(elektronik çek)", "Mailed check(posta çeki) ",
            "Bank transfer (automatic) / otomatik havale",
            "Credit card (automatic) / kredi kartı ile otomatik ödeme"
        ])

    st.subheader("Ek Servisler")
    # Not: Yeni modelde bazıları kullanılmasa da görsel bütünlük için burada bıraktık.
    c1, c2, c3, c4 = st.columns(4)
    with c1: online_security = st.selectbox("Online Güvenlik", ["Hayır", "Evet"])
    with c2: online_backup = st.selectbox("Online Yedekleme", ["Hayır", "Evet"])
    with c3: device_protection = st.selectbox("Cihaz Koruması", ["Hayır", "Evet"])
    with c4: tech_support = st.selectbox("Teknik Destek", ["Hayır", "Evet"])

    submit_btn = st.form_submit_button("Analiz Et")

# ---------------------------------------------------------
# TAHMİN İŞLEMİ (YENİ MODEL UYUMLU)
# ---------------------------------------------------------
if submit_btn:
    # Kullanıcı verisini df'e dönüştürme
    input_data = pd.DataFrame(index=[0])

    # Sayısal Değerleri Atama
    input_data['tenure'] = tenure
    input_data['MonthlyCharges'] = monthly_charges
    input_data['TotalCharges'] = total_charges


    # Yardımcı Fonksiyon
    def binary_map(val):
        return 1 if val == "Evet" else 0


    # Encoding İşlemleri
    input_data['SeniorCitizen_encode'] = binary_map(senior_citizen)
    input_data['Partner_encode'] = binary_map(partner)
    input_data['Dependents_encode'] = binary_map(dependents)
    input_data['OnlineSecurity_encode'] = binary_map(online_security)
    input_data['OnlineBackup_encode'] = binary_map(online_backup)
    input_data['DeviceProtection_encode'] = binary_map(device_protection)
    input_data['TechSupport_encode'] = binary_map(tech_support)
    input_data['PaperlessBilling_encode'] = binary_map(paperless_billing)

    # DİKKAT: Yeni analizinde Gender, PhoneService, StreamingTV, StreamingMovies çıkarıldı.
    # Bu yüzden onları burada input_data'ya eklemiyoruz, model zaten beklemiyor.

    # Ordinal Mapping
    internet_map = {"Yok": 0, "DSL": 1, "Fiber optic": 2}
    input_data['InternetService_encode'] = internet_map[internet_service]

    contract_map = {"aydan-aya": 0, "12 ay taahhüt": 1, "24 ay taahhüt": 2}
    input_data['Contract_encode'] = contract_map[contract]

    # One-Hot Encoding (Payment) - Modeldeki isimlerle eşleşmeli
    pay_methods = [
        'PaymentMethod_Bank transfer (automatic)',
        'PaymentMethod_Credit card (automatic)',
        'PaymentMethod_Electronic check',
        'PaymentMethod_Mailed check'
    ]
    for col in pay_methods:
        input_data[col] = 0  # Önce hepsini 0 yap

    # Seçileni 1 yap
    if "Bank transfer" in payment_method:
        sel_pay = 'PaymentMethod_Bank transfer (automatic)'
    elif "Credit card" in payment_method:
        sel_pay = 'PaymentMethod_Credit card (automatic)'
    elif "Electronic check" in payment_method:
        sel_pay = 'PaymentMethod_Electronic check'
    else:
        sel_pay = 'PaymentMethod_Mailed check'

    input_data[sel_pay] = 1

    # Sütun hizalama (Modelin eğitildiği sütun sırasıyla aynı olmalı)
    # Eksik sütun kalırsa 0 ile doldurur, fazla varsa atar.
    input_data = input_data.reindex(columns=model_columns, fill_value=0)

    # Tahmin
    try:
        # XGBoost scale edilmemiş veri ile de çalışır, scaler kaldırdık.
        prob = model.predict_proba(input_data)[0][1]  # Churn Olasılığı

        # Eşik Değeri
        ui_threshold = 0.50
        prediction = 1 if prob >= ui_threshold else 0

        st.write("---")
        st.subheader("Sonuç:")

        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.metric("Churn Olasılığı", f"%{prob * 100:.2f}")

        with c_res2:
            if prediction == 1:
                st.error("⚠️ RİSKLİ (CHURN)")
                st.write(f"Model, müşterinin %{prob * 100:.1f} ihtimalle ayrılacağını düşünüyor.")
            else:
                st.success("✅ GÜVENLİ (NO CHURN)")
                st.write(f"Müşteri güvende görünüyor. (Risk: %{prob * 100:.1f})")

        st.progress(float(prob))

    except Exception as e:
        st.error(f"Tahmin sırasında hata oluştu: {e}")
