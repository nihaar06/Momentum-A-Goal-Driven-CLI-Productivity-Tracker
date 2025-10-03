# app.py
import streamlit as st
from services import services
from db import ops

# --- Page Configuration ---
st.set_page_config(page_title="Momentum Tracker", layout="wide")
st.title("🚀 Momentum: Your Productivity Tracker")

# --- Initialize Backend ---
service_handler = services()
db_handler = ops()

# --- Sidebar Navigation ---
menu_choice = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Goal Management", "Time Tracking"]
)

# --- Page Content ---
if menu_choice == "Dashboard":
    st.header("Dashboard")
    st.write("Welcome! Here's a summary of your progress.")
    # You could add metrics and charts here

elif menu_choice == "Goal Management":
    st.header("🎯 Goal Management")

    # Display existing goals in a table
    st.subheader("Your Goals")
    all_goals = db_handler.list_goals()
    if all_goals:
        st.dataframe(all_goals)
    else:
        st.info("No goals found. Add one below!")

    # Add a new goal using a form
    with st.form("new_goal_form", clear_on_submit=True):
        st.subheader("Add a New Goal")
        desc = st.text_input("Goal Description")
        metric = st.selectbox("Metric", ["hours", "tasks"])
        target = st.number_input("Target Value", min_value=1)
        
        submitted = st.form_submit_button("Add Goal")
        if submitted:
            db_handler.add_goal(desc, metric, target, None)
            st.success("Goal added successfully!")

elif menu_choice == "Time Tracking":
    st.header("⏱️ Time Tracking")
    st.write("Time tracking features will be implemented here.")
    # You would add buttons to start/stop timers and forms to add tasks