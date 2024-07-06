import streamlit as st

def render():
    st.title("Step 3: Test Generation")
    st.write("Based on the provided data, the following API tests have been generated:")

    # Retrieve endpoints from session state
    if 'selected_cve' in st.session_state and 'endpoints' in st.session_state:
        endpoints = st.session_state.endpoints
    else:
        st.error("No endpoints found. Please complete the previous steps first.")
        return

    test_descriptions = [
        f"Test 1: Validate the response of {endpoints[0]} with sample payloads.",
        f"Test 2: Check the authentication and authorization for {endpoints[1]}.",
        f"Test 3: Ensure data integrity and response time for {endpoints[2]}.",
        f"Test 4: Verify the update of resource in {endpoints[0]} after applying the patch.",
        f"Test 5: Validate error handling for invalid inputs in {endpoints[1]}.",
        f"Test 6: Check the backward compatibility for {endpoints[2]}.",
        f"Test 7: Ensure correct logging for all requests to {endpoints[0]}.",
        f"Test 8: Test the rate limiting and throttling policies on {endpoints[1]}.",
        f"Test 9: Validate the data schema returned by {endpoints[2]}.",
        f"Test 10: Perform security testing to ensure no vulnerabilities in {endpoints[0]}."
    ]

    for test in test_descriptions:
        st.write(f"- {test}")

    if st.button("Back to Remediation"):
        st.session_state.current_step = 2
        st.experimental_rerun()
    
    if st.button("Mitigation and tests"):
        st.session_state.test_results = generate_mock_test_results(st.session_state.selected_cve, endpoints)
        st.session_state.current_step = 4
        st.experimental_rerun()

def generate_mock_test_results(cve, endpoints):
    package_name = cve['package']
    old_version = f"{package_name} v{cve['version']}"
    new_version = f"{package_name} v{cve['remediation_version']}"

    test_results = {
        "pass_fail_comparison": [
            {"Test": "Test 1", old_version: "Pass", new_version: "Pass"},
            {"Test": "Test 2", old_version: "Fail", new_version: "Pass"},
            {"Test": "Test 3", old_version: "Pass", new_version: "Pass"},
            {"Test": "Test 4", old_version: "Fail", new_version: "Fail"},
            {"Test": "Test 5", old_version: "Pass", new_version: "Pass"},
            {"Test": "Test 6", old_version: "Pass", new_version: "Fail"},
            {"Test": "Test 7", old_version: "Pass", new_version: "Pass"},
            {"Test": "Test 8", old_version: "Fail", new_version: "Pass"},
            {"Test": "Test 9", old_version: "Pass", new_version: "Pass"},
            {"Test": "Test 10", old_version: "Pass", new_version: "Fail"},
        ],
        "performance_comparison": [
            {"Metric": "Response Time (ms)", old_version: 120, new_version: 110},
            {"Metric": "Memory Usage (MB)", old_version: 512, new_version: 490},
            {"Metric": "CPU Usage (%)", old_version: 30, new_version: 25},
        ],
        "payload_comparison": [
            {"Endpoint": endpoints[0], old_version: "{'query': 'error logs', 'date_range': 'last 24 hours'}", new_version: "{'query': 'error logs', 'date_range': 'last 24 hours'}"},
            {"Endpoint": endpoints[1], old_version: "{'log_id': '12345', 'format': 'json'}", new_version: "{'log_id': '12345', 'format': 'json'}"},
            {"Endpoint": endpoints[2], old_version: "{'log_level': 'debug', 'output': 'console'}", new_version: "{'log_level': 'info', 'output': 'file'}"},
        ]
    }
    return test_results
