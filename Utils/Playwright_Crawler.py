import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# Set page configuration
st.set_page_config(page_title="POSSM Demo", layout="wide")

# Load assets
logo = Image.open("path_to_your_logo.png")

# Sidebar with navigation
st.sidebar.image(logo, use_column_width=True)
st.sidebar.title("POSSM Demo")
page = st.sidebar.radio("Navigate", [
    "Dashboard", 
    "Behavioral Monitoring", 
    "eBPF-Based Analysis", 
    "Vulnerability Identification", 
    "Real-Time Alerts", 
    "Exploit and Impact Assessment"
])

# Mock data for behavioral changes
behavioral_changes = pd.DataFrame({
    'Package': ['Package A', 'Package B'],
    'Change': ['Unusual access', 'Unexpected modification']
})

# Mock data for network traffic
network_traffic = pd.DataFrame({
    'Type': ['Incoming', 'Outgoing'],
    'Traffic': [1200, 1300]
})

# Function to display code snippet
def show_code_snippet(package):
    if package == 'Package A':
        code_before = """
        // Old version
        if (user.isAuthenticated()) {
            accessResource();
        }
        """
        code_after = """
        // New version
        accessResource();
        """
        anomaly = "Removed authentication check."
    elif package == 'Package B':
        code_before = """
        // Old version
        public void updateData(String data) {
            if (data != null) {
                this.data = data;
            }
        }
        """
        code_after = """
        // New version
        public void updateData(String data) {
            this.data = data;
        }
        """
        anomaly = "Removed null check, which could lead to null pointer exceptions."

    st.code(f"Before:\n{code_before}\n\nAfter:\n{code_after}", language='java')
    st.warning(f"Behavioral Anomaly: {anomaly}")

# Dashboard
if page == "Dashboard":
    st.title("POSSM - Proactive Open Source Security Monitor")
    st.header("Dashboard")
    st.write("Welcome to the POSSM demo. Use the navigation on the left to explore different features of the product.")
    st.markdown("### Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Vulnerabilities", "15", "3")
    col2.metric("Active Alerts", "5", "-1")
    col3.metric("Monitored Packages", "120", "5")

# Behavioral Monitoring
elif page == "Behavioral Monitoring":
    st.title("Proactive Security Monitoring")
    st.markdown("### Detected Behavioral Changes")
    st.table(behavioral_changes)

    selected_package = st.selectbox('Select a package to view details', behavioral_changes['Package'])

    if st.button('Show Code Snippet'):
        show_code_snippet(selected_package)

# eBPF-Based Environment Analysis
elif page == "eBPF-Based Analysis":
    st.title("eBPF-Based Environment Analysis")
    st.markdown("### Network Traffic Analysis")
    traffic_chart = alt.Chart(network_traffic).mark_bar().encode(
        x='Type',
        y='Traffic',
        color='Type'
    )
    st.altair_chart(traffic_chart, use_container_width=True)

# Run the app using: streamlit run possm_demo.py
