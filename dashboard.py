import streamlit as st
import pandas as pd
import plotly.express as px
from db import ops
from services import services

ss=services()
op=ops()

def display_dashboard():
    st.subheader("Today's Summary")
    # 1. Fetch the raw data for today
    today_raw_data = ss.track_activity(days=0)

    if not today_raw_data.empty:
        # 2. FIX: Add this line to group the data and sum the minutes per category
        today_summary = today_raw_data.groupby('category')['duration_minutes'].sum()

        # 3. Now, get the single values from the aggregated summary
        prod_time = today_summary.get('productive', 0)
        dist_time = today_summary.get('distracting', 0)

        # 4. The rest of your code will now work correctly with single numbers
        total_active_time = prod_time + dist_time
        score = (prod_time / total_active_time * 100) if total_active_time > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Productive Time", f"{prod_time} min")
        col2.metric("Distracting Time", f"{dist_time} min")
        col3.metric("Productivity Score", f"{score:.1f}%")
    else:
        st.info("No activity logged today to generate metrics.")
    st.subheader("📊 Activity Dashboard")
    graph=st.selectbox('Visual Analysis',['Bar Chart','Line Chart','Pie Chart'])
    d=st.selectbox('Last N days',['Today','Last 7 Days','Last 30 Days'])
    day_map = {'Today': 0, 'Last 7 Days': 7, 'Last 30 Days': 30}
    day = day_map[d]
    ###BAR CHART###
    if graph=='Bar Chart':
        st.subheader(f"📈App Usage Trend (Last {d})")
        data=ss.track_activity(day)
        if data.empty:
            st.info(f"No activity logged for the selected period.")
        else:
            summ=data.groupby('category')['duration_minutes'].sum().reset_index()
            st.bar_chart(summ.set_index('category'))
    ###LINE CHART###
    elif graph=='Line Chart':
        c=st.selectbox('Category',['Neutral','Productive','Distracting'])
        st.subheader(f"📈 {c} App Usage Trend (Last {d})")
        data=ss.track_productivity(category=c.lower(),days=day)
        if data.empty:
            st.info(f"No activity logged for the last {day} days")
        chart_data=data.set_index('date')
        st.line_chart(chart_data)
        st.write(f"This chart shows the total minutes of {c} activity logged for the last {day} days.")
    ###PIE CHART###
    elif graph=='Pie Chart':
        st.subheader(f"📈App Usage Trend (Last {d})")
        data=ss.track_activity(day)
        if data.empty:
            st.info(f"No activity logged for the selected period.")
        else:
            summary = data.groupby('category')['duration_minutes'].sum().reset_index()
            fig=px.pie(summary,names='category',values='duration_minutes',title='Time Distribution')
            st.plotly_chart(fig,use_container_width=True)
    # In app.py, inside the 'if page == "Dashboard":' block

    # --- Display Recent Activity Logs (with Aggregation) ---
    with st.expander("View Recent Activity Logs"):
        # We can reuse the data we fetched for the charts
        # The 'day' variable is already defined from your chart selectbox
        raw_activity_data = ss.track_activity(day)
    
        if raw_activity_data.empty:
            st.write("No activity logs for this period.")
        else:
            # 1. Add a radio button to let the user choose the view
            view_choice = st.radio(
                "Select View Type:",
                ('Aggregated View', 'Detailed View'),
                horizontal=True,
                label_visibility='collapsed'
            )
    
            # 2. Show the detailed view (the single table you already had)
            if view_choice == 'Detailed View':
                st.subheader("Detailed Log")
                st.write("Showing every individual log entry for the selected period.")
                st.dataframe(raw_activity_data, use_container_width=True)
            
            # 3. Show the new aggregated view
            elif view_choice == 'Aggregated View':
                st.subheader("Aggregated Summary")
                st.write("Showing total time spent per window title.")
                
                # Use pandas to group by the window title and sum the minutes
                aggregated_df = raw_activity_data.groupby('window_title')['duration_minutes'].sum().sort_values(ascending=False).reset_index()
                
                # Rename columns for better readability
                aggregated_df.rename(columns={'duration_minutes': 'Total Minutes'}, inplace=True)
                
                st.dataframe(aggregated_df, use_container_width=True)
    st.subheader("Prioritized Tasks")
    tasks=ss.get_prioritized_tasks()
    if not tasks:
        st.info("No prioritized tasks found.")
    else:
        df_tasks=pd.DataFrame(tasks)
        st.dataframe(df_tasks,use_container_width=True)