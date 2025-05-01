import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset and train dummy model for placeholder
def load_data():
    df = pd.read_csv('telecom_churn.csv')  # Replace with actual path
    df['date_of_registration'] = pd.to_datetime(df['date_of_registration'], errors='coerce')
    df['days_from_registration'] = (pd.Timestamp.today() - df['date_of_registration']).dt.days
    df.drop(['customer_id', 'pincode', 'date_of_registration', 'gender', 'state', 'city', 'telecom_partner'], axis=1, inplace=True)
    return df

df = load_data()
X = df.drop('churn', axis=1)
y = df['churn']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = RandomForestClassifier().fit(X_scaled, y)

# Streamlit App
st.title("Telecom Churn Prediction App")
menu = ["Overview", "EDA", "Model Comparison", "Feature Importance", "Predict Churn"]
choice = st.sidebar.selectbox("Select Tab", menu)

if choice == "Overview":
    st.header("Data Overview")
    st.write(df.head())
    st.write("Summary Statistics:")
    st.write(df.describe())

elif choice == "EDA":
    st.header("Exploratory Data Analysis")
    plt.figure(figsize=(5,4))
    sns.countplot(data=df, x='churn')
    plt.title('Churn Distribution')
    plt.show()

    plt.figure(figsize=(6, 4))
    churn_rate = df.groupby('telecom_partner')['churn'].mean().sort_values(ascending=False)
    sns.barplot(x=churn_rate.index, y=churn_rate.values)
    plt.title(f'Churn Rate by Telecom Partner')
    plt.ylabel('Churn Rate')
    plt.tight_layout()
    plt.show()

    st.subheader("Correlation Matrix (Excluding Churn)")
    corr = df.drop('churn', axis=1).corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    df.drop(columns=['customer_id', 'pincode', 'date_of_registration', 'state', 'city'], inplace=True)

    # Split features and target
    X = df.drop('churn', axis=1)
    y = df['churn']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify= y, test_size=0.2, random_state=42)

    # Label encode categorical columns (after split)
    cat_cols = X.select_dtypes(include='object').columns
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        X_train[col] = le.fit_transform(X_train[col])
        X_test[col] = le.transform(X_test[col])
        label_encoders[col] = le

    # Standard scale numeric features (after encoding)
    num_cols = ['age', 'num_dependents', 'estimated_salary', 'calls_made', 'sms_sent', 'data_used']
    scaler = StandardScaler()
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    # Random Forest with class imbalance handling
    rf = RandomForestClassifier(n_estimators=60, class_weight='balanced', random_state=42).fit(X_train, y_train)

    # Feature importance
    st.header("Feature Importance")
    importances = rf.feature_importances_
    features = X_train.columns
    importance_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=False)

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=importance_df, x='Importance', y='Feature')
    plt.title('Feature Importance (Balanced, Scaled)')
    plt.tight_layout()
    plt.show()

elif choice == "Model Comparison":
    st.header("Model Performance")
    st.write("XGBoost:\nF1-Score: 0.32\nRecall: 0.80")
    st.write("Random Forest:\nF1-Score: 0.32\nRecall: 0.66")
    st.write("Logistic Regression:\nF1-Score: 0.29\nRecall: 0.50")
    st.write("KNN:\nF1-Score: 0.14\nRecall: 0.11")
    st.write("Gaussian NB:\nF1-Score: 0.00\nRecall: 0.00")


elif choice == "Predict Churn":
    st.header("Predict Customer Churn")
    data_used = st.number_input("Data Used (GB)", min_value=0.0, value=5.0)
    sms_sent = st.number_input("SMS Sent", min_value=0, value=50)
    calls_made = st.number_input("Calls Made", min_value=0, value=100)
    days_from_registration = st.number_input("Days Since Registration", min_value=0, value=365)
    estimated_salary = st.number_input("Salary", min_value=0, value=85000)

    input_data = pd.DataFrame([[ data_used, sms_sent, calls_made, days_from_registration, estimated_salary]],
                               columns=['data_used', 'sms_sent', 'calls_made', 'days_from_registration', 'estimated_salary'])
    input_scaled = scaler.transform(input_data)
    prediction = rf.predict(input_scaled)

    if st.button("Predict"):
        if prediction[0] == 1:
            st.error("The customer is likely to churn.")
        else:
            st.success("The customer is not likely to churn.")
