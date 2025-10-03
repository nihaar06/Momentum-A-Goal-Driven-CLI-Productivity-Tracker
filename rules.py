import streamlit as st
import pandas as pd
import plotly.express as px
from db import ops
from services import services

ss=services()
op=ops()

def display_rules():
    st.subheader("⚙️ Manage Categorization Rules")
    
    st.subheader("Current Rules")
    all_rules = ss.get_all_rules()
    if not all_rules:
        st.info("No rules defined.")
    else:
        st.dataframe(pd.DataFrame(all_rules), use_container_width=True)

    with st.expander("Add or Delete a Rule"):
        # Form to add a new rule
        with st.form("new_rule_form", clear_on_submit=True):
            st.subheader("Add a New Rule")
            keyword = st.text_input("Keyword (e.g., YouTube, VS Code)")
            category = st.selectbox("Category", ["productive", "distracting", "neutral"])
            if st.form_submit_button("Add Rule"):
                ss.add_rule(keyword, category)
                st.success(f"Rule for '{keyword}' added!")
                st.rerun()

        # Section to delete a rule
        st.subheader("Delete a Rule")
        if all_rules:
            rule_options = {f"{r['rule_id']}: {r['keyword']}": r['rule_id'] for r in all_rules}
            rule_to_delete_desc = st.selectbox("Select a rule to delete:", rule_options.keys())
            if st.button("Delete Selected Rule", type="primary"):
                rule_id_to_delete = rule_options[rule_to_delete_desc]
                ss.delete_rule(rule_id_to_delete)
                st.warning(f"Rule {rule_id_to_delete} has been deleted.")
                st.rerun()
