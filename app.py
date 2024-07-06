import streamlit as st
from pages import step1, step2, step3, step4

st.set_page_config(layout="wide", page_title="CVE Remediation Wizard")

# Initialize session state variables
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "selected_cve" not in st.session_state:
    st.session_state.selected_cve = None
if "additional_data" not in st.session_state:
    st.session_state.additional_data = {"files": None, "info": "", "user_journeys": []}
if "test_results" not in st.session_state:
    st.session_state.test_results = None

def render_steps():
    steps = [
        {"title": "CVE List", "func": step1.render},
        {"title": "Remediation", "func": step2.render},
        {"title": "Test Generation", "func": step3.render},
        {"title": "Mitigation and Tests Results", "func": step4.render}
    ]
    
    for index, step in enumerate(steps):
        step_title = step["title"]
        if index + 1 == st.session_state.current_step:
            #st.subheader(step_title)
            step["func"]()

# Main render logic
render_steps()
