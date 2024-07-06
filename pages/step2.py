import streamlit as st
import pandas as pd
import random
from streamlit_agraph import agraph, Node, Edge, Config


def render_user_journey_map(user_journeys,service):
     # Visualize the user journeys
        nodes = []
        edges = []
        node_ids = set()
        
        for i, journey in enumerate(user_journeys):
            user_node = Node(id=f"user_{i+1}", label=f"User{i+1}", shape="dot", size=15)
            if user_node.id not in node_ids:
                nodes.append(user_node)
                node_ids.add(user_node.id)
            
            steps = journey["journey"].split(" -> ")
            for j, step in enumerate(steps):
                endpoint_node = Node(id=step, label=f"{step}\n({service})", shape="dot", size=15)
                if endpoint_node.id not in node_ids:
                    nodes.append(endpoint_node)
                    node_ids.add(endpoint_node.id)
                
                if j == 0:
                    edges.append(Edge(source=user_node.id, target=endpoint_node.id, label=""))
                else:
                    edges.append(Edge(source=steps[j-1], target=endpoint_node.id, label=step))

        config = Config(width=800, height=600, directed=True, nodeHighlightBehavior=True, highlightColor="#F7A7A6", collapsible=False)
        return agraph(nodes=nodes, edges=edges, config=config)
    


def generate_endpoints(service_name, package_name):
    # Map services and packages to realistic endpoints
    if service_name == "Log Management Service" :
        return [
            "/api/logs/search",
            "/api/logs/download",
            "/api/logs/configure"
        ]
    elif service_name == "Authentication Service" :
        return [
            "/api/auth/login",
            "/api/auth/register",
            "/api/auth/refresh"
        ]
    elif service_name == "Data Processing Service" :
        return [
            "/api/data/transform",
            "/api/data/analyze",
            "/api/data/report"
        ]
    elif service_name == "Payment Gateway Service" :
        return [
            "/api/payments/create",
            "/api/payments/refund",
            "/api/payments/history"
        ]
    else:
        return ["/api/default/endpoint1", "/api/default/endpoint2", "/api/default/endpoint3"]

def generate_user_journeys(service_name, endpoints):
    if service_name == "Log Management Service":
        user_journeys = [
            {"user": "User1", "journey": f"{endpoints[0]} -> {endpoints[1]}", "payload": "{'query': 'error logs', 'date_range': 'last 24 hours'}"},
            {"user": "User2", "journey": f"{endpoints[1]} -> {endpoints[2]}", "payload": "{'log_id': '12345', 'format': 'json'}"},
            {"user": "User3", "journey": f"{endpoints[0]} -> {endpoints[2]}", "payload": "{'query': 'access logs', 'user': 'admin'}"}
        ]
    elif service_name == "Authentication Service":
        user_journeys = [
            {"user": "User1", "journey": f"{endpoints[0]} -> {endpoints[2]}", "payload": "{'username': 'john_doe', 'password': 'securePass123'}"},
            {"user": "User2", "journey": f"{endpoints[1]} -> {endpoints[0]}", "payload": "{'username': 'jane_doe', 'email': 'jane@example.com'}"},
            {"user": "User3", "journey": f"{endpoints[0]} -> {endpoints[1]}", "payload": "{'username': 'user123', 'refresh_token': 'abcdef123456'}"}
        ]
    elif service_name == "Data Processing Service":
        user_journeys = [
            {"user": "User1", "journey": f"{endpoints[0]} -> {endpoints[1]}", "payload": "{'data': 'raw_data.csv', 'operation': 'clean'}"},
            {"user": "User2", "journey": f"{endpoints[1]} -> {endpoints[2]}", "payload": "{'data': 'cleaned_data.csv', 'analysis_type': 'summary'}"},
            {"user": "User3", "journey": f"{endpoints[2]} -> {endpoints[0]}", "payload": "{'report_id': '7890', 'format': 'pdf'}"}
        ]
    elif service_name == "Payment Gateway Service":
        user_journeys = [
            {"user": "User1", "journey": f"{endpoints[0]} -> {endpoints[2]}", "payload": "{'amount': '100.00', 'currency': 'USD', 'method': 'credit_card'}"},
            {"user": "User2", "journey": f"{endpoints[1]} -> {endpoints[0]}", "payload": "{'transaction_id': 'txn_12345', 'reason': 'product_return'}"},
            {"user": "User3", "journey": f"{endpoints[2]} -> {endpoints[1]}", "payload": "{'user_id': 'user789', 'history': 'last_month'}"}
        ]
    else:
        user_journeys = [
            {"user": "User1", "journey": f"{endpoints[0]} -> {endpoints[1]}", "payload": "{'key': 'value1'}"},
            {"user": "User2", "journey": f"{endpoints[1]} -> {endpoints[2]}", "payload": "{'key': 'value2'}"},
            {"user": "User3", "journey": f"{endpoints[2]} -> {endpoints[0]}", "payload": "{'key': 'value3'}"}
        ]
    return user_journeys

def render():
    st.title("Remediation and Testing")

    if 'selected_cve' not in st.session_state or st.session_state.selected_cve is None:
        st.error("No CVE selected. Please go back to the CVE List page.")
        st.session_state.current_step = 1
        st.experimental_rerun()
    else:
        cve = st.session_state.selected_cve
        data = {
            "CVE": [cve['id']],
            "Service": [cve['service']],
            "Package": [cve['package']],
            "Current Version": [cve['version'] ],
            "Remediation Version": [cve['remediation_version']],
            "Severity": [cve['severity']],
            "CVSS Score": [cve['cvss']],
            "Reachability": [cve['reachability']],
        }

        df = pd.DataFrame(data)
        st.table(df)

        # Section 1: Affected Area
        st.subheader("Affected Area")
        st.write(f"According to our scan, we found that the following endpoints are affected by this {cve['package']} update:")
        endpoints = generate_endpoints(cve['service'], cve['package'])
        st.session_state.endpoints = endpoints
        for endpoint in endpoints:
            st.write(f"- {endpoint}")

        # Section 2: Additional Data
        st.subheader("Additional data that we can better suit the tests")
        st.write("Upload files that can help describe the functional and business logic of this service and context:")
        uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True, key="additional_files")
        additional_info = st.text_area("Additional Info", key="additional_info")

        # Section 3: User Journeys
        st.subheader("Top 3 User Journeys based on the endpoints relevant to this package")
        user_journeys = generate_user_journeys(cve['service'],endpoints)
        user_journey_df = pd.DataFrame(user_journeys)
        st.dataframe(user_journey_df)

        # Render the user journey visualization using D3.js
        render_user_journey_map(user_journeys,cve['service'])

        # for journey in user_journeys:
        #     st.write(f"**{journey['user']}**: {journey['journey']} with payload {journey['payload']}")

        if st.button("Generate Tests"):
            st.session_state.additional_data["files"] = uploaded_files
            st.session_state.additional_data["info"] = additional_info
            st.session_state.additional_data["user_journeys"] = user_journeys
            st.session_state.current_step = 3
            st.experimental_rerun()

        if st.button("Back to CVE List"):
            st.session_state.current_step = 1
            st.experimental_rerun()
