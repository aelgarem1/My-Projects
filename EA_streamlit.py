import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Load Dataset
@st.cache_data
def load_data():
    file_path = "HR-Employee-Attrition.xlsx"  # Upload the dataset
    df = pd.read_excel(file_path)
    return df

df = load_data()

# Sidebar Navigation
st.sidebar.title("Employee Attrition Analysis")
tab = st.sidebar.radio("Select Section", ["EDA", "Model Comparison", "Insights"])

# 🟢 EDA Tab
if tab == "EDA":
    st.title("Exploratory Data Analysis (EDA)")
    
    # Show dataset
    if st.checkbox("Show Raw Dataset"):
        st.write(df.head())

    # Class Balance
    st.subheader("Class Balance")
    attrition_counts = df['Attrition'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=attrition_counts.index, y=attrition_counts.values, palette="coolwarm")
    ax.set_title("Attrition Class Distribution")
    st.pyplot(fig)
    
    # Feature Types
    numerical_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df.select_dtypes(include=['object']).columns.tolist()

    st.subheader("Feature Types")
    st.write(f"Numerical Features: {numerical_features}")
    st.write(f"Categorical Features: {categorical_features}")

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(df.corr(numeric_only= True), cmap="coolwarm", annot=False, linewidths=0.5)
    st.pyplot(fig)

# 🟢 Model Comparison Tab
elif tab == "Model Comparison":
    st.title("Model Accuracy Comparison")

    # Preprocess Data
    df_cleaned = df.drop(columns=['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber'])
    categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
    label_encoders = {}

    for col in categorical_cols:
        le = LabelEncoder()
        df_cleaned[col] = le.fit_transform(df_cleaned[col])
        label_encoders[col] = le

    # Define Features and Target
    X = df_cleaned.drop(columns=['Attrition'])
    y = df_cleaned['Attrition']

    # Handle Multicollinearity using VIF
    def calculate_vif(df):
        vif_data = pd.DataFrame()
        vif_data["Feature"] = df.columns
        vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
        return vif_data

    vif_df = calculate_vif(X)
    high_vif_features = vif_df[vif_df["VIF"] > 10]["Feature"].tolist()
    X_reduced = X.drop(columns=high_vif_features)

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_reduced, y, test_size=0.2, random_state=42, stratify=y)

    # Train Random Forest Model
    rf_model = RandomForestClassifier(class_weight='balanced', random_state=42, n_estimators=100)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    acc_rf = accuracy_score(y_test, y_pred_rf)

    # Train Logistic Regression Model
    log_model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
    log_model.fit(X_train, y_train)
    y_pred_log = log_model.predict(X_test)
    acc_log = accuracy_score(y_test, y_pred_log)

    # Compare Model Accuracies
    st.subheader("Model Accuracies")
    st.write(f"Random Forest Accuracy: {acc_rf:.4f}")
    st.write(f"Logistic Regression Accuracy: {acc_log:.4f}")

    # Show Classification Reports
    st.subheader("Classification Reports")
    report_dict = classification_report(y_test, y_pred_rf, output_dict = True)
    report_df = pd.DataFrame(report_dict).transpose()
    st.text("classification Report for Random Forest Model")
    st.dataframe(report_df)
    
    report_dict2 = classification_report(y_test, y_pred_log)
    report_df2 =  pd.DataFrame(report_dict2).transpose()
    st.subheader("Classification Report for Logistic Regression Model")
    st.dataframe(report_df2)
    
# 🟢 Insights Tab
elif tab == "Insights":
    st.title("Key Insights & Takeaways")

    st.subheader("Findings from EDA")
    st.write("""
    - The dataset is **highly imbalanced**, with only 16% of employees experiencing attrition.
    - Several numerical features exhibit high correlation (e.g., Monthly Income, Job Level, and Total Working Years).
    - Features with high **multicollinearity** were removed using **VIF analysis**.
    """)

    st.subheader("Model Performance Comparison")
    st.write("""
    - **Random Forest performed better** due to its ability to capture complex interactions.
    - **Logistic Regression had lower accuracy** but is still useful for interpretation.
    - Both models used **class weighting** to handle the imbalance issue.
    """)

    st.subheader("Business Recommendations")
    st.write("""
    - Focus on employees with **lower job satisfaction** and **higher distance from home**.
    - Offer **better work-life balance** and **training programs** to retain talent.
    - Monitor employees with **fewer years at the company** or **frequent job changes**.
    """)



