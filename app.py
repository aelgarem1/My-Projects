import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier



st.sidebar.title("About Me")
st.sidebar.markdown("""
**Amira El-Garem**  
*Business Intelligence Developer*  
Passionate about data science, analytics, and solving real-world problems using data-driven approaches.
""")


def load_data():
    df = pd.read_csv('telecom_churn.csv')  
    df['num_dependents'] = df['num_dependents'].astype(str)
    df['churn'] = df['churn'].astype(str)
    return df

df = load_data()


st.title("Telecom Churn Prediction App")
menu = ["Overview", "EDA", "Model Comparison", "Predict Churn"]
choice = st.sidebar.selectbox("Select Tab", menu)

if choice == "Overview":
    st.header("Data Overview")
    st.write(df.head())
   

    # Data shape
    st.write(f"**Dataset Shape:** {df.shape[0]} rows, {df.shape[1]} columns")

    st.write("**Summary Statistics:**")
    st.write(df.describe(exclude= 'object'))

    st.write("**Null Values & Data Types:**")
    buffer = pd.DataFrame({
        'Column': df.columns,
        'Non-Null Count': df.notnull().sum().values,
        'Data Type': df.dtypes.values
    })
    st.write(buffer)

elif choice == "EDA":
    st.header("Exploratory Data Analysis")
    st.subheader("Churn Distribution")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.countplot(data=df, x='churn',  hue='churn', palette='Set2', ax=ax1)
    ax1.set_xlabel('')
    ax1.set_ylabel('')
    ax1.legend(title='Churn Status', labels=['Non-Churn (0)', 'Churn (1)'])
    st.pyplot(fig1)

    df['churn'] = df['churn'].astype(int)
    churn_rate = df.groupby('telecom_partner')['churn'].mean().sort_values(ascending=False)
    st.subheader("Churn Rate by Telecom Partner")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=churn_rate.index, y=churn_rate.values, hue = churn_rate.index, ax=ax2)
    ax2.set_xlabel('')
    ax2.set_ylabel('')
    st.pyplot(fig2)

    st.subheader("Correlation Matrix")
    df = pd.read_csv('telecom_churn.csv')
    df['date_of_registration'] = pd.to_datetime(df['date_of_registration'], errors='coerce')
    df['days_from_registration'] = (pd.Timestamp.today() - df['date_of_registration']).dt.days


    df['call_frequency'] = df['calls_made'] / df['days_from_registration']
    df['sms_frequency'] = df['sms_sent'] / df['days_from_registration']
    df['data_usage_frequency'] = df['data_used'] / df['days_from_registration']

# Drop irrelevant columns
    df.drop(columns=[
        'customer_id', 'pincode', 'state', 'city', 'date_of_registration', 'num_dependents',
        'calls_made', 'sms_sent', 'data_used', 'days_from_registration'
    ], inplace=True)

    df_numeric = df.select_dtypes(exclude=['object'])
    corr = df_numeric.drop('churn', axis=1).corr()
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.set_xlabel('')
    ax3.set_ylabel('')
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax3)
    st.pyplot(fig3)

    df = load_data()
    df['date_of_registration'] = pd.to_datetime(df['date_of_registration'])
    df['days_from_registration'] = (pd.Timestamp.today() - df['date_of_registration']).dt.days
    df['calls_frequency'] = df['calls_made'] / df['days_from_registration']
    df['sms_frequency'] = df['sms_sent'] / df['days_from_registration']
    df['data_usage_frequency'] = df['data_used'] / df['days_from_registration']
    df.drop(['customer_id', 'pincode','state', 'city', 'date_of_registration', 'days_from_registration'], axis=1, inplace=True)

    X = df.drop('churn', axis=1)
    y = df['churn']


    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify= y, test_size=0.2, random_state=42)

    cat_cols = X.select_dtypes(include='object').columns
    label_encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        X_train[col] = le.fit_transform(X_train[col])
        X_test[col] = le.transform(X_test[col])
        label_encoders[col] = le

    num_cols = ['age', 'num_dependents', 'estimated_salary', 'calls_frequency', 'sms_frequency', 'data_usage_frequency']
    scaler = StandardScaler()
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    rf = RandomForestClassifier(n_estimators=60, class_weight='balanced', random_state=42).fit(X_train, y_train)
    importances = rf.feature_importances_
    features = X_train.columns
    importance_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=False)
    colors = sns.color_palette("coolwarm", len(importance_df))

    st.subheader("Feature Importance By Random Forest Classifier")
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=importance_df, x='Importance', y='Feature', palette= colors, ax=ax4)
    ax4.set_xlabel('')
    ax4.set_ylabel('')
    st.pyplot(fig4)

elif choice == "Model Comparison":
    st.header("Model Performance")
    model_results = pd.DataFrame({
        'Model': ['XGBoost', 'Random Forest', 'Logistic Regression', 'KNN', 'Gaussian NB'],
        'F1-Score': [0.32, 0.32, 0.29, 0.14, 0.00],
        'Recall': [0.80, 0.66, 0.50, 0.11, 0.00]
    })
    st.table(model_results)



elif choice == "Predict Churn":
    st.header("Predict Customer Churn")
    data_usage_frequency = st.number_input("Data Used Per Day (GB)", min_value=0.0, value=5.0)
    sms_frequency = st.number_input("SMS Sent Per Day", min_value=0, value=50)
    calls_frequency = st.number_input("Calls Made Per Day", min_value=0, value=100)
    estimated_salary = st.number_input("Salary", min_value=0, value=85000)

    input_data = pd.DataFrame([[  estimated_salary, calls_frequency, sms_frequency, data_usage_frequency]],
                               columns=[ 'estimated_salary', 'call_frequency', 'sms_frequency', 'data_usage_frequency'])
    scaler = StandardScaler()

    df = load_data()
    df['churn'] = df['churn'].astype(int)


    df['date_of_registration'] = pd.to_datetime(df['date_of_registration'])
    df['days_from_registration'] = (pd.Timestamp.today() - df['date_of_registration']).dt.days
    df['call_frequency'] = df['calls_made'] / df['days_from_registration']
    df['sms_frequency'] = df['sms_sent'] / df['days_from_registration']
    df['data_usage_frequency'] = df['data_used'] / df['days_from_registration']
    df.drop(['customer_id', 'pincode','state', 'city', 'date_of_registration', 'num_dependents' , 'gender','age', 'telecom_partner','days_from_registration', 'data_used', 'sms_sent', 'calls_made'], axis=1, inplace=True)


    X = df.drop('churn', axis=1)
    y = df['churn']

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)



    imbalance_ratio = (y_train == 0).sum() / (y_train == 1).sum()


    model = XGBClassifier(
            eval_metric='logloss',
            random_state=42,
            n_estimators=60,
            max_depth= 2,
            learning_rate=0.01,
            scale_pos_weight = imbalance_ratio)

    model.fit(X_train, y_train)

    input_scaled = scaler.fit_transform(input_data)

    prediction = model.predict(input_scaled)

    if st.button("Predict"):
        if prediction[0] == 1:
            st.error("The customer is likely to churn.")
        else:
            st.success("The customer is not likely to churn.")
