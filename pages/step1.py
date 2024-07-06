import streamlit as st

def render():
    st.title("CVE List")
    st.write("Select a CVE to auto-remediate and test:")

    # Sample CVE data for demonstration
    
    cve_data = [
    {
        'id': 'CVE-2021-44228',
        'service': 'Log Management Service',
        'package': 'log4j',
        'version': '2.14.0',
        'remediation_version': '2.15.0',
        'severity': 'Critical',
        'cvss': 10.0,
        'reachability': 'Yes'
    },
    {
        'id': 'CVE-2021-34527',
        'service': 'Authentication Service',
        'package': 'auth0',
        'version': '1.0.0',
        'remediation_version': '1.1.0',
        'severity': 'High',
        'cvss': 8.8,
        'reachability': 'Yes'
    },
    {
        'id': 'CVE-2021-3156',
        'service': 'Data Processing Service',
        'package': 'pandas',
        'version': '1.2.0',
        'remediation_version': '1.2.1',
        'severity': 'High',
        'cvss': 7.5,
        'reachability': 'Yes'
    },
    {
        'id': 'CVE-2021-21972',
        'service': 'Payment Gateway Service',
        'package': 'stripe',
        'version': '6.7.0',
        'remediation_version': '6.7.1',
        'severity': 'Critical',
        'cvss': 9.8,
        'reachability': 'Yes'
    },
]

    for cve in cve_data:
        with st.expander(f"{cve['id']} - {cve['service']}"):
            st.write(f"**Service:** {cve['service']}")
            st.write(f"**Package:** {cve['package']}")
            st.write(f"**Current Version:** {cve['version']}")
            st.write(f"**Remediation Version:** {cve['remediation_version']}")
            st.write(f"**Severity:** {cve['severity']}")
            st.write(f"**CVSS Score:** {cve['cvss']}")
            st.write(f"**Reachability:** {cve['reachability']}")
            if st.button(f"Remediate {cve['id']}"):
                st.session_state.selected_cve = cve
                st.session_state.current_step = 2
                st.experimental_rerun()
