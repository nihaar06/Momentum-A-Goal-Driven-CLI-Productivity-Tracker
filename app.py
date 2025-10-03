import streamlit as st
import pandas as pd
import plotly.express as px
from db import ops
from services import services

st.set_page_config(page_title='Momentum Tracker',layout='wide')
st.title("🚀 Momentum: Your Productivity Tracker")

ss=services()
op=ops()

page=st.sidebar.radio('NAVIGATION',['Dashboard','Goals','Tasks'])
if page=='Dashboard':
    st.title(" Activity Dashboard")
    graph=st.selectbox('Visual Analysis',['Bar Chart','Line Chart','Pie Chart'])
    ###BAR CHART###
    if graph=='Bar Chart':
        d=st.selectbox('Last N days',['1 Day','7 Days','30 Days'])
        st.subheader(f"📈App Usage Trend (Last {d})")
        if d=='1 Day':
            day=1
        elif d=='7 Days':
            day=7
        else :
            day=30
        data=ss.track_activity(day)
        if data.empty:
            st.info(f"No activity logged for the selected period.")
        else:
            summ=data.groupby('category')['duration_minutes'].sum().reset_index()
            st.bar_chart(summ.set_index('category'))
    ###LINE CHART###
    elif graph=='Line Chart':
        c=st.selectbox('Category',['Neutral','Productive','Distracting'])
        d=st.selectbox('Last N days',['1 Day','7 Days','30 Days'])
        st.subheader(f"📈 {c} App Usage Trend (Last {d})")
        if d=='1 Day':
            day=1
        elif d=='7 Days':
            day=7
        else :
            day=30
        data=ss.track_productivity(category=c.lower(),days=day)
        if data.empty:
            st.info(f"No activity logged for the last {day} days")
        chart_data=data.set_index('date')
        st.line_chart(chart_data)
        st.write(f"This chart shows the total minutes of {c} activity logged for the last {day} days.")
    ###PIE CHART###
    elif graph=='Pie Chart':
        d=st.selectbox('Last N days',['1 Day','7 Days','30 Days'])
        st.subheader(f"📈App Usage Trend (Last {d})")
        if d=='1 Day':
            day=1
        elif d=='7 Days':
            day=7
        else :
            day=30
        data=ss.track_activity(day)
        if data.empty:
            st.info(f"No activity logged for the selected period.")
        else:
            summary = data.groupby('category')['duration_minutes'].sum().reset_index()
            fig=px.pie(summary,names='category',values='duration_minutes',title='Time Distribution')
            st.plotly_chart(fig,use_container_width=True)
    
    st.subheader("Prioritized Tasks:")
    prdf=pd.DataFrame(ss.get_prioritized_tasks())
    if prdf.empty:
        st.info("No prioritized tasks found.")
    else:
        st.dataframe(prdf)
elif page == "Goals":
    st.subheader("🎯 Goal Management")
    gdf=ss.list_goals()
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
elif page == "Tasks":
    st.subheader("⏱️ Task Management")
    tdf=ss.list_tasks()
    if not tdf:
        st.info("No tasks found.")
    else:
        df_tasks=pd.DataFrame(tdf)
        st.dataframe(df_tasks,use_container_width=True)
    with st.expander("Add new task"):
        with st.form("NEW_TASK_FORM",clear_on_submit=True):
            st.subheader("Add a new Task")
            new_gid = st.number_input("Goal ID:", min_value=1, step=1)
            new_desc=st.text_input("Description:")
            new_is_prioritized=st.selectbox("Prioritized",['True','False'])
            submitted=st.form_submit_button("Add Task")
            if submitted:
                is_prioritized_bool = (new_is_prioritized == 'True') 
                ss.add_task(int(new_gid),new_desc,is_prioritized_bool)
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