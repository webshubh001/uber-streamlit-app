# Uber Rides Data Analysis - Streamlit App (with Login, Multipage Navigation & Themed UI)

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

# Inject custom CSS for themed UI
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f8;
        }
        .stApp {
            background-color: #ffffff;
        }
        .css-1d391kg, .css-1lcbmhc {
            color: #1e3a8a !important;  /* navy blue headers */
        }
        .stButton>button {
            background-color: #1e3a8a;
            color: white;
            border-radius: 5px;
        }
        .stDownloadButton>button {
            background-color: #059669;
            color: white;
            border-radius: 5px;
        }
        .css-ffhzg2, .css-1kyxreq {
            color: #4b5563 !important;  /* muted text */
        }
        .css-145kmo2, .css-1aumxhk {
            background-color: #e0f2fe !important;
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
        
        **Use the sidebar to navigate. Upload your dataset to begin.**
    """)

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    uploaded_file = st.sidebar.file_uploader("📂 Upload Uber CSV File", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        page = st.sidebar.radio("📊 Navigate to", ["Welcome", "Overview", "Trips Over Time", "Trip Categories", "Distance Analysis", "Edit & Export"])

        if page == "Welcome":
            welcome()

        elif page == "Overview":
            st.title("📋 Data Overview")
            st.write(df.head(50))
            st.success(f"Total trips: {len(df)}")

        elif page == "Trips Over Time":
            st.title("📅 Trips Over Time")
            df['date'] = df['start_date'].dt.date
            daily = df.groupby('date').size()
            fig, ax = plt.subplots()
            daily.plot(ax=ax)
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Trips")
            st.pyplot(fig)

        elif page == "Trip Categories":
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

        elif page == "Distance Analysis":
            st.title("📏 Trip Distance Distribution")
            fig, ax = plt.subplots()
            sns.histplot(df['miles'], bins=30, color='skyblue', ax=ax)
            ax.set_xlabel("Miles")
            ax.set_ylabel("Trips")
            st.pyplot(fig)

        elif page == "Edit & Export":
            st.title("✏️ Edit & Export Dataset")
            editable = df.copy()
            edited_df = st.data_editor(editable, num_rows="dynamic")
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
# Uber Rides Data Analysis - Streamlit App (with Login, Multipage Navigation & Themed UI)

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

# Inject custom CSS for themed UI
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f8;
        }
        .stApp {
            background-color: #ffffff;
        }
        .css-1d391kg, .css-1lcbmhc {
            color: #1e3a8a !important;  /* navy blue headers */
        }
        .stButton>button {
            background-color: #1e3a8a;
            color: white;
            border-radius: 5px;
        }
        .stDownloadButton>button {
            background-color: #059669;
            color: white;
            border-radius: 5px;
        }
        .css-ffhzg2, .css-1kyxreq {
            color: #4b5563 !important;  /* muted text */
        }
        .css-145kmo2, .css-1aumxhk {
            background-color: #e0f2fe !important;
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
        
        **Use the sidebar to navigate. Upload your dataset to begin.**
    """)

# Initialize login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    uploaded_file = st.sidebar.file_uploader("📂 Upload Uber CSV File", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        page = st.sidebar.radio("📊 Navigate to", ["Welcome", "Overview", "Trips Over Time", "Trip Categories", "Distance Analysis", "Edit & Export"])

        if page == "Welcome":
            welcome()

        elif page == "Overview":
            st.title("📋 Data Overview")
            st.write(df.head(50))
            st.success(f"Total trips: {len(df)}")

        elif page == "Trips Over Time":
            st.title("📅 Trips Over Time")
            df['date'] = df['start_date'].dt.date
            daily = df.groupby('date').size()
            fig, ax = plt.subplots()
            daily.plot(ax=ax)
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Trips")
            st.pyplot(fig)

        elif page == "Trip Categories":
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

        elif page == "Distance Analysis":
            st.title("📏 Trip Distance Distribution")
            fig, ax = plt.subplots()
            sns.histplot(df['miles'], bins=30, color='skyblue', ax=ax)
            ax.set_xlabel("Miles")
            ax.set_ylabel("Trips")
            st.pyplot(fig)

        elif page == "Edit & Export":
            st.title("✏️ Edit & Export Dataset")
            editable = df.copy()
            edited_df = st.data_editor(editable, num_rows="dynamic")
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
