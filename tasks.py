import streamlit as st
import pandas as pd
import plotly.express as px
from db import ops
from services import services

ss=services()
op=ops()


def display_tasks():
    st.subheader("⏱️ Task Management")
    tdf=ss.list_tasks()
    if not tdf:
        st.info("No tasks found.")
    else:
        df_tasks=pd.DataFrame(tdf)
        st.dataframe(df_tasks,use_container_width=True)
    with st.expander("Add new task"):
        # First, fetch all existing goals to populate the dropdown
        all_goals = op.list_goals()

        if not all_goals:
            st.warning("You must create a goal before you can add a task. Go to the 'Goals' page.")
        else:
            with st.form("NEW_TASK_FORM", clear_on_submit=True):
                st.subheader("Add a new Task")

                # FIX: Use a selectbox instead of a number input
                selected_goal = st.selectbox(
                    "Link to Goal:",
                    all_goals,
                    # This function tells the selectbox what to display to the user
                    format_func=lambda goal: f"{goal['goal_id']}: {goal['description']}"
                )

                new_desc = st.text_input("Description:")
                new_is_prioritized = st.checkbox("Prioritize this task?")

                submitted = st.form_submit_button("Add Task")
                if submitted:
                    # Get the actual ID from the full goal object the user selected
                    goal_id = selected_goal['goal_id']
                    ss.add_task(goal_id, new_desc, new_is_prioritized)
                    st.success("Task Added successfully.")
                    st.rerun()
    if tdf: # Only show this section if there are tasks to manage
        st.subheader("Edit or Delete a Task")
        
        # Create a user-friendly list of tasks for the selectbox
        task_options = {f"{t['task_id']}: {t['description']}": t['task_id'] for t in tdf}
        selected_task_desc = st.selectbox("Select a task to manage:", task_options.keys())
        
        if selected_task_desc:
            selected_task_id = task_options[selected_task_desc]
            # Fetch the full data for the selected task
            selected_task_data = op.get_task(selected_task_id)

            with st.form(f"edit_task_{selected_task_id}"):
                st.write(f"**Editing Task ID: {selected_task_id}**")
                
                # Form fields pre-filled with the task's current data
                new_desc = st.text_input("Description", value=selected_task_data['description'])
                new_gid = st.number_input("Goal ID", min_value=1, value=selected_task_data['goal_id'])
                
                # Update and Delete buttons
                update_btn, delete_btn = st.columns(2)
                with update_btn:
                    if st.form_submit_button("Update Task"):
                        op.update_task(selected_task_id, new_desc, new_gid)
                        st.success(f"Task {selected_task_id} updated.")
                        st.rerun()
                with delete_btn:
                    if st.form_submit_button("Delete Task", type="primary"):
                        op.delete_task(selected_task_id)
                        st.warning(f"Task {selected_task_id} deleted.")
                        st.rerun()