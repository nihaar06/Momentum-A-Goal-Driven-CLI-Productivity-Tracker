import streamlit as st
import pandas as pd
import plotly.express as px
from db import ops
from services import services
from datetime import datetime

ss=services()
op=ops()


def display_goals():
    st.subheader("🎯 Goal Management")
    gdf=ss.list_goals()
    st.subheader("Urgent Goals")
    if not gdf:
        st.info("No goals found. Add one below to get started!")
    else:
        today = datetime.now().date()
        # Filter for goals that have a future deadline
        upcoming_goals = [
            g for g in gdf 
            if g.get('deadline') and datetime.strptime(g['deadline'], '%Y-%m-%d').date() >= today
        ]

        if not upcoming_goals:
            st.success("🎉 No upcoming deadlines! You're all caught up.")
        else:
            # Sort the goals by the deadline to find the nearest one
            nearest_goal = sorted(upcoming_goals, key=lambda g: g['deadline'])[0]
            deadline_date = datetime.strptime(nearest_goal['deadline'], '%Y-%m-%d').date()
            days_remaining = (deadline_date - today).days

            # Display the alert
            st.warning(
                f"🚨 **Deadline Alert:** Your most urgent goal is **'{nearest_goal['description']}'**, "
                f"due in **{days_remaining} day(s)!**"
            )

    # --- NEW: Interactive Goal List with Progress Bars ---
    st.subheader("Your Current Goals")
    if gdf:
        # Display headers for our custom table
        col1, col2, col3 = st.columns([3, 2, 3])
        col1.markdown("**Goal Description**")
        col2.markdown("**Progress**")
        col3.markdown("**Progress Bar**")
        st.divider()

        for goal in gdf:
            # Calculate progress, handling division by zero
            target = goal['target_value']
            current = goal['current_value']
            progress_percent = (current / target) if target > 0 else 0
            
            col1, col2, col3 = st.columns([3, 2, 3])
            with col1:
                st.write(goal['description'])
            with col2:
                st.write(f"{current} / {target} {goal['metric']}")
            with col3:
                st.progress(progress_percent)
    if not gdf:
        st.info("No goals found.")
    else:
        df_goals = pd.DataFrame(gdf)[['goal_id', 'description', 'metric', 'current_value', 'target_value','deadline']]
        st.dataframe(df_goals,use_container_width=True)
    with st.expander("Add a new goal"):
        with st.form("NEW_GOAL_FORM",clear_on_submit=True):
            st.subheader("Add a New Goal")
            desc=st.text_input("Goal Description:")
            m=st.selectbox("Metric",['Tasks','Hours'])
            target=st.number_input("Target Value",min_value=1,step=1)
            deadline = st.date_input("Deadline (Optional)", value=None)
            submitted=st.form_submit_button("Add Goal")
            if submitted:
                ss.add_goal(desc,m,target,str(deadline) if deadline else None)
                st.success("Goal added successfully.")
                st.rerun()
    if gdf:
        st.subheader("Update or Delete Existing Goals")
        goal_options={f"{g['goal_id']}:{g['description']}":g['goal_id'] for g in gdf}
        selected_goal_desc=st.selectbox("Select a goal to manage:",goal_options.keys())
        if selected_goal_desc:
            selected_goal_id=goal_options[selected_goal_desc]
            selected_goal_data=ss.get_goal(selected_goal_id)
            with st.form(f"edit_goal_{selected_goal_id}"):
                st.write(f"**Editing Goal ID:{selected_goal_id}**")
                new_desc=st.text_input("Description",value=selected_goal_data['description'])
                metric_options = ['hours', 'tasks'] 
                new_metric = st.selectbox(
                    'Metric', 
                    metric_options,     
                    index=metric_options.index(selected_goal_data['metric'].lower())
                )
                new_target=st.number_input('Target Value',min_value=1,value=selected_goal_data['target_value'])

                col1,col2=st.columns(2)
                with col1:
                    update_submitted=st.form_submit_button("Update Goal")
                with col2:
                    delete_submitted=st.form_submit_button("Delete Goal",type="primary")
                if update_submitted:
                    ss.update_goal(selected_goal_id,new_desc,new_metric,new_target)
                    st.success(f"Goal {selected_goal_id} updated successfully.")
                if delete_submitted:
                    st.session_state.confirm_delete = st.checkbox("Yes, I want to permanently delete this goal.")
                    if st.session_state.confirm_delete:
                        ss.delete_goal(selected_goal_id)
                        st.warning(f"Goal {selected_goal_id} has been deleted.")
                        del st.session_state.confirm_delete
                        st.rerun()