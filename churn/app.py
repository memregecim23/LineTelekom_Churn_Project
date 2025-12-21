import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, MinMaxScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import os

# Sayfa Ayarları
st.set_page_config(
    page_title="LİNETELEKOM A.Ş CHURN ANALİZ SİSTEMİ",
    layout="centered"
)

# Model Eğitimi

current_dir = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(current_dir, "Churn.csv")

try:
    dfChurn = pd.read_csv(csv_path)
except FileNotFoundError:
    csv_path_backup = os.path.join(current_dir, "WA_Fn-UseC_-Telco-Customer-Churn.csv")
    dfChurn = pd.read_csv(csv_path_backup)

    # Veri Ön İşleme

    # TotalCharges düzenleme
    dfChurn["TotalCharges"] = pd.to_numeric(dfChurn["TotalCharges"], errors='coerce')
    dfChurn["TotalCharges"] = dfChurn["TotalCharges"].fillna(2700.0)
    dfChurn["TotalCharges"] = dfChurn["TotalCharges"].astype(float)

    # Label Encoding yapılacakları direkt düşüyoruz (Senin yöntem)
    columns_to_labelencode = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
        "StreamingTV", "StreamingMovies", "PaperlessBilling", "Churn", "MultipleLines"
    ]

    # Target (Churn) Encode
    dfChurn["Churn_encode"] = dfChurn["Churn"].apply(lambda x: 1 if x == "Yes" else 0)

    # Ordinal Encoding
    ordinal_internetservices = OrdinalEncoder(categories=[["No", "DSL", "Fiber optic"]])
    ordinal_contract = OrdinalEncoder(categories=[["Month-to-month", "One year", "Two year"]])

    dfChurn["InternetService_encode"] = ordinal_internetservices.fit_transform(dfChurn[["InternetService"]])
    dfChurn["Contract_encode"] = ordinal_contract.fit_transform(dfChurn[["Contract"]])

    # One-Hot Encoding (PaymentMethod)
    dfChurnencode = pd.get_dummies(dfChurn, columns=["PaymentMethod"])

    drop_cols = ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
                 "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
                 "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
                 "StreamingMovies", "Contract", "PaperlessBilling", "Churn"]

    # Hata almamak için sadece var olanları düşürür
    dfChurnencode.drop([c for c in drop_cols if c in dfChurnencode.columns], axis=1, inplace=True)

    cols_to_map = ["SeniorCitizen", "Partner", "Dependents", "OnlineSecurity",
                   "OnlineBackup", "DeviceProtection", "TechSupport", "PaperlessBilling"]

    # Orijinal df'den değerleri alıp map eder
    for col in cols_to_map:
        # SeniorCitizen zaten 0-1, diğerleri Yes-No
        if col == "SeniorCitizen":
            dfChurnencode[f"{col}_encode"] = dfChurn[col]
        else:
            dfChurnencode[f"{col}_encode"] = dfChurn[col].apply(lambda x: 1 if x == "Yes" else 0)


    # X ve y ayrımı
    X = dfChurnencode.drop(["Churn_encode"], axis=1)
    y = dfChurnencode["Churn_encode"]

    # Eğitim
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=15)

    scaler = MinMaxScaler()
    X_trainscale = scaler.fit_transform(X_train)

    svc = SVC(kernel="rbf", class_weight="balanced", probability=True)
    svc.fit(X_trainscale, y_train)

    return svc, scaler, X.columns, "OK"


# Fonksiyonu çalıştır
model, scaler, model_columns, status = train_model_live()

# Streamlit Arayüzü

if status == "CSV":
    st.error("🚨 HATA: 'WA_Fn-UseC_-Telco-Customer-Churn.csv' dosyası bulunamadı!")
    st.warning("Lütfen CSV dosyasını bu python dosyasının olduğu klasöre atın.")
    st.stop()

st.title("📉 LİNETELEKOM İŞTE-İŞ CHURN ANALİZ UYGULAMASI")

with st.form("churn_form"):
    st.header("Müşteri Bilgileri")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hizmet & Sözleşme")
        tenure = st.number_input("Müşteri Süresi(AY)", min_value=0,value=12)
        monthly_charges = st.number_input("Aylık Ücret(küsüratlı giriniz)", min_value=100.5,value=220.5)
        total_charges = st.number_input("Toplam Ücret(küsüratlı giriniz)", min_value=100.5,value=1700.5)

        contract = st.selectbox("Sözleşme Türü", ["aydan-aya", "12 ay taahhüt", "24 ay taahhüt"])
        internet_service = st.selectbox("İnternet Servisi", ["Yok", "DSL", "Fiber optic"])

    with col2:
        st.subheader("Kişisel & Fatura")
        senior_citizen = st.selectbox("Yaşlı Vatandaş mı?", ["Hayır", "Evet"])
        partner = st.selectbox("Partneri Var mı?", ["Hayır", "Evet"])
        dependents = st.selectbox("Bakmakla Yükümlü?", ["Hayır", "Evet"])
        paperless_billing = st.selectbox("Kağıtsız Fatura?", ["Hayır", "Evet"])
        payment_method = st.selectbox("Ödeme Yöntemi", [
            "Electronic check(elektronik çek)", "Mailed check(posta çeki) ", "Bank transfer (automatic) / otomatik havale", "Credit card (automatic) / kredi kartı ile otomatik ödeme"
        ])

    st.subheader("Ek Servisler")
    c1, c2, c3, c4 = st.columns(4)
    with c1: online_security = st.selectbox("Online Güvenlik", ["Hayır", "Evet"])
    with c2: online_backup = st.selectbox("Online Yedekleme", ["Hayır", "Evet"])
    with c3: device_protection = st.selectbox("Cihaz Koruması", ["Hayır", "Evet"])
    with c4: tech_support = st.selectbox("Teknik Destek", ["Hayır", "Evet"])

    submit_btn = st.form_submit_button("Analiz Et")

# TAHMİN

if submit_btn:
    # Kullanıcı verisini df'e döüştürme
    input_data = pd.DataFrame(index=[0])

    # Değerleri Atama
    input_data['tenure'] = tenure
    input_data['MonthlyCharges'] = monthly_charges
    input_data['TotalCharges'] = total_charges


    # Binary Mapping
    def binary_map(val):
        return 1 if val == "Evet" else 0


    input_data['SeniorCitizen_encode'] = binary_map(senior_citizen)
    input_data['Partner_encode'] = binary_map(partner)
    input_data['Dependents_encode'] = binary_map(dependents)
    input_data['OnlineSecurity_encode'] = binary_map(online_security)
    input_data['OnlineBackup_encode'] = binary_map(online_backup)
    input_data['DeviceProtection_encode'] = binary_map(device_protection)
    input_data['TechSupport_encode'] = binary_map(tech_support)
    input_data['PaperlessBilling_encode'] = binary_map(paperless_billing)

    # Ordinal Mapping
    internet_map = {"Yok": 0, "DSL": 1, "Fiber optic": 2}
    input_data['InternetService_encode'] = internet_map[internet_service]

    contract_map = {"aydan-aya": 0, "12 ay taahhüt": 1, "24 ay taahhüt": 2}
    input_data['Contract_encode'] = contract_map[contract]

    # One-Hot Encoding (Payment)
    pay_methods = [
        'PaymentMethod_Bank transfer (automatic)',
        'PaymentMethod_Credit card (automatic)',
        'PaymentMethod_Electronic check',
        'PaymentMethod_Mailed check'
    ]
    for col in pay_methods: input_data[col] = 0

    sel_pay = f"PaymentMethod_{payment_method}"
    if sel_pay in pay_methods: input_data[sel_pay] = 1

    # Sütun hizalama (Eğitimdeki X sütunlarına göre)
    input_data = input_data.reindex(columns=model_columns, fill_value=0)

    # Ölçeklendirme ve Tahmin
    try:
        input_scaled = scaler.transform(input_data)
        prob = model.predict_proba(input_scaled)[0][1]  # Churn Olasılığı


        # Modelin optimali 0.25 olsa da, Arayüzde %50 (0.50) kullanıyoruz.
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
            else:
                st.success("✅ GÜVENLİ (NO CHURN)")

        st.progress(prob)

    except Exception as e:

        st.error(f"Hata: {e}")

