# Uber Rides Data Analysis - Streamlit App 

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(
    page_title="Uber Rides Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for dark mode with menu bar layout
st.markdown(
    """
    <style>
        body {
            background-color: #111827;
            color: #f9fafb;
        }
        .stApp {
            background-color: #1f2937;
            padding: 2rem;
        }
        .css-1d391kg, .css-1lcbmhc, .css-ffhzg2, .css-1kyxreq {
            color: #f9fafb !important;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        .stDownloadButton>button {
            background-color: #10b981;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
        }
        .css-145kmo2, .css-1aumxhk {
            background-color: #374151 !important;
            color: white !important;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Login credentials
USER_CREDENTIALS = {"admin": "admin123", "user": "uber2024"}

@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
    df = df.dropna(subset=['start_date', 'miles'])
    return df

# Login page
def login():
    st.title("🔐 Uber Data Portal - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Welcome page
def welcome():
    st.title("🚗 Welcome to Uber Rides Explorer")
    st.markdown("""
        This dashboard gives insights into ride distances, timing trends, trip purposes, and more.

        **Upload your dataset using the uploader above to begin.**
    """)

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    st.title("📊 Uber Rides Dashboard")
    uploaded_file = st.file_uploader("📂 Upload Uber CSV File", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        selected_page = st.selectbox("Choose Analysis Section", ["Welcome", "Overview", "Trips Over Time", "Trip Categories", "Distance Analysis", "Edit & Export"])

        if selected_page == "Welcome":
            welcome()

        elif selected_page == "Overview":
            st.title("📋 Data Overview")
            st.dataframe(df.head(50), use_container_width=True)
            st.success(f"Total trips: {len(df)}")

        elif selected_page == "Trips Over Time":
            st.title("📅 Trips Over Time")
            df['date'] = df['start_date'].dt.date
            daily = df.groupby('date').size()
            fig, ax = plt.subplots(figsize=(10, 4))
            daily.plot(ax=ax)
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Trips")
            st.pyplot(fig)

        elif selected_page == "Trip Categories":
            st.title("📂 Trip Purpose & Category")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("By Purpose")
                if 'purpose' in df.columns:
                    st.bar_chart(df['purpose'].value_counts())
                else:
                    st.warning("Purpose column missing.")

            with col2:
                st.subheader("By Category")
                if 'category' in df.columns:
                    st.bar_chart(df['category'].value_counts())
                else:
                    st.warning("Category column missing.")

        elif selected_page == "Distance Analysis":
            st.title("📏 Trip Distance Distribution")
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.histplot(df['miles'], bins=30, color='orange', ax=ax)
            ax.set_xlabel("Miles")
            ax.set_ylabel("Trips")
            st.pyplot(fig)

        elif selected_page == "Edit & Export":
            st.title("✏️ Edit & Export Dataset")
            editable = df.copy()
            edited_df = st.data_editor(editable, num_rows="dynamic", use_container_width=True)
            st.success("You can edit the table above. Scroll to view all rows.")

            buffer = BytesIO()
            edited_df.to_csv(buffer, index=False)
            st.download_button(
                label="📥 Download Edited Data as CSV",
                data=buffer.getvalue(),
                file_name="edited_uber_data.csv",
                mime="text/csv"
            )
    else:
        st.warning("Please upload a CSV file to get started.")
