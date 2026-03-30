import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.processing import AttendanceProcessor
from src.model import AttendanceAnomalyDetector
from src.visuals import (
    plot_duration_distribution,
    plot_login_vs_duration,
    plot_anomalies_by_department,
    plot_top_employees,
    plot_anomaly_heatmap
)

# Page config
st.set_page_config(
    page_title="Attendance Anomaly Detector",
    page_icon="🕒",
    layout="wide"
)

# Theme/CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stMetric {
        background-color: #1e1e1e;
        color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# App Title & Header
st.title("🛡️ Attendance Anomaly Detection")
st.markdown("Automated anomaly detection in employee logs using Isolation Forest.")

# Sidebar - Settings & File Upload
st.sidebar.header("📁 Data Settings")
uploaded_file = st.sidebar.file_uploader("Upload Attendance CSV", type=["csv"])

contamination = st.sidebar.slider(
    "Contamination (Anomaly Rate)", 
    0.01, 0.20, 0.05, 
    help="Expected percentage of anomalies in the dataset."
)

st.sidebar.markdown("---")
st.sidebar.info(""" 
**Features Analyzed:**
- Login/Logout times
- Total shift duration
- Login deviation from 9 AM
- Weekend work patterns
- Departmental behaviors
""")

# Sample Data Button
if not uploaded_file:
    st.info("💡 Pro-tip: You can use the generated sample data at `data/attendance_sample.csv`.")
    if st.button("Load Sample Data"):
        uploaded_file = "/home/vk-linux/Desktop/attendance/data/attendance_sample.csv"

# Main Logic
if uploaded_file:
    try:
        # Load
        df_raw = pd.read_csv(uploaded_file)
        
        # Display Statistics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records", len(df_raw))
        col2.metric("Total Employees", df_raw['employee_id'].nunique())
        col3.metric("Departments", df_raw['department'].nunique())
        
        # 1. Dataset Preview (Requirement)
        with st.expander("📄 Raw Data Preview", expanded=False):
            st.write("First 10 records of the uploaded file:")
            st.dataframe(df_raw.head(10), use_container_width=True)
            
        # 2. Feature Engineering Output (Requirement)
        with st.status("Performing Feature Engineering...", expanded=False) as status:
            processor = AttendanceProcessor()
            df_display, df_processed = processor.process(df_raw)
            status.update(label="Features Engineered successfully!", state="complete")
        
        with st.expander("⚙️ Processed Features Preview", expanded=False):
            st.write("Numerical features generated for the model (Minutes since midnight, etc.):")
            st.dataframe(df_processed.head(10), use_container_width=True)

        st.markdown("---")

        # 3. Model Training
        st.subheader("🤖 Model Control")
        if st.button("🚀 Train Model & Detect Anomalies"):
            with st.spinner("Analyzing patterns..."):
                detector = AttendanceAnomalyDetector(contamination=contamination)
                anomalies = detector.fit_predict(df_processed)
                df_display['is_anomaly'] = anomalies
                
                # Insights calculation
                normal_stats = df_display[df_display['is_anomaly'] == 0].median(numeric_only=True)
                df_display['reason'] = df_display.apply(
                    lambda row: detector.explain_anomaly(row, normal_stats) if row['is_anomaly'] == 1 else "",
                    axis=1
                )
                
                st.session_state['results'] = df_display
                st.success(f"Detected {sum(anomalies)} potential anomalies!")

        # Results Visualization
        if 'results' in st.session_state:
            res_df = st.session_state['results']
            anomaly_df = res_df[res_df['is_anomaly'] == 1]
            
            # Key Metric update
            col4.metric("Anomalies Found", len(anomaly_df), delta_color="inverse")
            
            # Tabs for organization
            tab1, tab2, tab3 = st.tabs(["📊 Visual Analysis", "📋 Detected Anomalies", "📈 Employee Trends"])
            
            with tab1:
                c1, c2 = st.columns(2)
                
                # Plot 1: Work Duration Distribution
                with c1:
                    st.subheader("Work Duration Distribution")
                    fig1 = plot_duration_distribution(res_df)
                    st.plotly_chart(fig1, use_container_width=True)
                
                # Plot 2: Login vs Duration Scatter
                with c2:
                    st.subheader("Login vs Work Duration")
                    fig2 = plot_login_vs_duration(res_df)
                    st.plotly_chart(fig2, use_container_width=True)

            with tab2:
                st.subheader("Anomaly Detailed List")
                st.write("Below are the flagged anomalies with generated reasons:")
                st.dataframe(
                    anomaly_df[['date', 'employee_id', 'department', 'total_work_minutes', 'reason']],
                    use_container_width=True
                )
                
                # Download CSV
                csv = anomaly_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Anomaly Report",
                    csv, "anomaly_report.csv", "text/csv"
                )

            with tab3:
                st.subheader("Anomalies by Department & Employee")
                c1, c2 = st.columns(2)
                
                with c1:
                    fig_dept = plot_anomalies_by_department(anomaly_df)
                    st.plotly_chart(fig_dept, use_container_width=True)
                    
                with c2:
                    fig_emp = plot_top_employees(anomaly_df)
                    st.plotly_chart(fig_emp, use_container_width=True)

                st.markdown("---")
                st.subheader("🗓️ Anomaly Density Heatmap")
                st.write("Understand which days of the week have the most irregular patterns per department.")
                
                fig_heat = plot_anomaly_heatmap(anomaly_df)
                if fig_heat:
                    st.plotly_chart(fig_heat, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    # Landing Page UI
    st.info("👋 Please upload a CSV file or load sample data from the sidebar to begin.")
    st.markdown("""
    ### 📋 CSV Requirements:
    The CSV should contain the following columns:
    - `employee_id`: Unique identifier for each employee.
    - `login_time`: Time of login in `HH:MM:SS` format.
    - `logout_time`: Time of logout in `HH:MM:SS` format.
    - `date`: Date of the record (`YYYY-MM-DD`).
    - `department`: Employee's department.
    """)
