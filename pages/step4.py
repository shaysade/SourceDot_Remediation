import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def render():
    st.title("Step 4: Mitigation and Tests Results")

    if not st.session_state.test_results:
        st.error("No test results available. Please complete the previous steps first.")
        st.session_state.current_step = 3
        st.experimental_rerun()
    else:
        test_results = st.session_state.test_results
        
        st.subheader("Pass/Fail Comparison")
        pass_fail_df = pd.DataFrame(test_results['pass_fail_comparison'])
        pass_fail_styler = pass_fail_df.style.apply(
            lambda x: ['background-color: red' if x.iloc[1] != x.iloc[2] else '' for i in range(len(x))], 
            axis=1)
        st.dataframe(pass_fail_styler)

        st.subheader("Performance Benchmark Comparison")
        performance_df = pd.DataFrame(test_results['performance_comparison'])
        performance_styler = performance_df.style.apply(
            lambda x: ['background-color: red' if x.iloc[1] < x.iloc[2] else '' for i in range(len(x))], 
            axis=1)
        st.dataframe(performance_styler)

        st.subheader("Payload Comparison")
        payload_df = pd.DataFrame(test_results['payload_comparison'])
        payload_styler = payload_df.style.apply(
            lambda x: ['background-color: red' if x.iloc[1] != x.iloc[2] else '' for i in range(len(x))], 
            axis=1)
        st.dataframe(payload_styler)

        # Extract old and new version column names
        columns = pass_fail_df.columns[1:]
        old_version, new_version = columns[0], columns[1]

        # Bar chart for Pass/Fail comparison
        st.subheader("Pass/Fail Summary")
        pass_counts_old = pass_fail_df.applymap(lambda x: x == "Pass").sum(axis=1).sum()
        pass_counts_new = pass_fail_df.applymap(lambda x: x == "Pass").sum(axis=0)[new_version]
        total_tests = len(pass_fail_df)
        pass_percentage_old = (pass_counts_old / total_tests) * 100
        pass_percentage_new = (pass_counts_new / total_tests) * 100

        fig, ax = plt.subplots()
        ax.bar(["Old Version", "New Version"], [pass_percentage_old, pass_percentage_new], color=["blue", "green"])
        ax.set_ylabel("Pass Percentage")
        ax.set_title("Pass Percentage Comparison")
        st.pyplot(fig)

        # Bar chart for performance comparison
        st.subheader("Performance Metrics")
        metrics = performance_df["Metric"]
        old_values = performance_df[performance_df.columns[1]]
        new_values = performance_df[performance_df.columns[2]]
        fig, ax = plt.subplots()
        ax.bar(metrics, old_values, width=0.4, label="Old Version", align="center")
        ax.bar(metrics, new_values, width=0.4, label="New Version", align="edge")
        ax.legend()
        st.pyplot(fig)

    if st.button("Back to Test Generation"):
        st.session_state.current_step = 3
        st.experimental_rerun()
