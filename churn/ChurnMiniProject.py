import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib

dfChurn = pd.read_csv("Churn.csv")

dfChurn.info()
dfChurn.isnull().sum()
dfChurn.head()
dfChurn.describe()
dfChurn.shape


# Null değerleri yaklaşık float değerle doldurup type dönüşümü yapıldı.
dfChurn["TotalCharges"].isnull().sum()
dfChurn["TotalCharges"] = pd.to_numeric(dfChurn["TotalCharges"], errors='coerce')
dfChurn["TotalCharges"] = dfChurn["TotalCharges"].fillna(2700.0)
dfChurn["TotalCharges"] = dfChurn["TotalCharges"].astype(float)
dfChurn.info()
dfChurn.value_counts()

# Label encoder ile (1-0) şeklinde object kolonlar encode edildi.
from sklearn.preprocessing import LabelEncoder
label = LabelEncoder()
dfChurn["gender_encode"] = label.fit_transform(dfChurn["gender"])
dfChurn["SeniorCitizen_encode"] = label.fit_transform(dfChurn["SeniorCitizen"])
dfChurn["Partner_encode"] = label.fit_transform(dfChurn["Partner"])
dfChurn["Dependents_encode"] = label.fit_transform(dfChurn["Dependents"])
dfChurn["PhoneService_encode"] = label.fit_transform(dfChurn["PhoneService"])
dfChurn["OnlineSecurity_encode"] = label.fit_transform(dfChurn["OnlineSecurity"])
dfChurn["OnlineBackup_encode"] = label.fit_transform(dfChurn["OnlineBackup"])
dfChurn["DeviceProtection_encode"] = label.fit_transform(dfChurn["DeviceProtection"])
dfChurn["TechSupport_encode"] = label.fit_transform(dfChurn["TechSupport"])
dfChurn["StreamingTV_encode"] = label.fit_transform(dfChurn["StreamingTV"])
dfChurn["StreamingMovies_encode"] = label.fit_transform(dfChurn["StreamingMovies"])
dfChurn["PaperlessBilling_encode"] = label.fit_transform(dfChurn["PaperlessBilling"])
dfChurn["Churn_encode"] = label.fit_transform(dfChurn["Churn"])
dfChurn["MultipleLines_encode"] = label.fit_transform(dfChurn["MultipleLines"])


#columns_to_encode = [
   # "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
   # "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
   # "StreamingTV", "StreamingMovies", "PaperlessBilling", "Churn"
#]

#new_column_names = [
   # "gender_encode", "SeniorCitizen_encode", "Partner_encode", "Dependents_encode",
   # "PhoneService_encode", "OnlineSecurity_encode", "OnlineBackup_encode",
   # "DeviceProtection_encode", "TechSupport_encode", "StreamingTV_encode",
   # "StreamingMovies_encode", "PaperlessBilling_encode", "Churn_encode"
#]

#for old_col, new_col in zip(columns_to_encode, new_column_names):
#if old_col in dfChurn.columns:
#dfChurn[new_col] = label.fit_transform(dfChurn[old_col])
# #else:
# print(f"Uyarı: '{old_col}' isimli sütun bulunamadı.")
#print(dfChurn[new_column_names].head())


dfChurn.info()
columns_to_labelencode = [
   "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
   "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
   "StreamingTV", "StreamingMovies", "PaperlessBilling", "Churn","MultipleLines"
]

#Encode sonrası eski kolonlar drop edildi.
dfChurn.drop(columns_to_labelencode,axis=1,inplace=True)
dfChurn["MultipleLines"].value_counts()
dfChurn.info()


dfChurn["InternetService"].value_counts()
dfChurn["Contract"].value_counts()

#Ordinal encoding uygulaması hiyerarşi bulunan kolonlara uygulandı.
from sklearn.preprocessing import OrdinalEncoder
ordinal_internetservices =OrdinalEncoder(categories=[["No","DSL","Fiber optic"]])
ordinal_contract = OrdinalEncoder(categories=[["Month-to-month","One year","Two year"]])
dfChurn["InternetService_encode"] = ordinal_internetservices.fit_transform(dfChurn[["InternetService"]])
dfChurn["Contract_encode"] = ordinal_contract.fit_transform(dfChurn[["Contract"]])

columns_to_ordinalencode = ["InternetService","Contract"]
dfChurn.drop(columns_to_ordinalencode,axis=1,inplace=True)
dfChurn.info()
dfChurn.head()
dfChurn["Contract_encode"] = dfChurn["Contract_encode"].astype(int)
dfChurn["InternetService_encode"] = dfChurn["InternetService_encode"].astype(int)
dfChurn.info()


#one-hot encoding uygulandı.
dfChurn["PaymentMethod"].value_counts()
dfChurnencode = pd.get_dummies(dfChurn,columns=["PaymentMethod"])
dfChurnencode.drop(["customerID"],axis=1,inplace=True)
dfChurnencode.info()
dfChurnencode.corr()["Churn_encode"].sort_values()

# Model sağlığı için düşük kolerasyonlu(modele etkisi değiştirmeyecek kadar olan) sütunlar drop edildi.
low_corr = [
    "gender_encode",
    "PhoneService_encode",
    "StreamingTV_encode",
    "StreamingMovies_encode",
    "MultipleLines_encode"
]
dfChurnencode.drop(columns=low_corr,axis=1,inplace=True)

# Model kurulum - Performans izleme aşamaları yapıldı.

X = dfChurnencode.drop(["Churn_encode"],axis=1)
y = dfChurnencode["Churn_encode"]


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=15)

from sklearn.preprocessing import MinMaxScaler
minmax = MinMaxScaler()
X_trainscale = minmax.fit_transform(X_train)
X_testscale = minmax.transform(X_test)

from sklearn.svm import SVC
svc = SVC(kernel="rbf", class_weight="balanced",probability=True)
svc.fit(X_trainscale,y_train)
y_pred_proba = svc.predict_proba(X_testscale)[:, 1]
yeni_esik = 0.25
y_pred_yeni = (y_pred_proba >= yeni_esik).astype(int)


from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
report = classification_report(y_test,y_pred_yeni)
matrix = confusion_matrix(y_test,y_pred_yeni)
accuracy = accuracy_score(y_test,y_pred_yeni)

print(matrix)
print(report)
print(accuracy)

# Model pkl dosyası olarak kaydedildi.

import joblib
modelpkl = {
    "model": svc,
    "threshold": yeni_esik,
    "scaler": minmax,
    "columns": X_train.columns.tolist()
}

joblib.dump(modelpkl, "telco_churn_model.pkl")

print("Model başarıyla paketlenip kaydedildi")
