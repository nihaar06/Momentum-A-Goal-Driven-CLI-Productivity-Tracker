"""
Momentum Tracker - Main Streamlit Application
Run this file to start the application: streamlit run app.py
"""

import streamlit as st
from src.dao import db
from src.services.services import services
from src.frontend.dashboard import display_dashboard
from src.frontend.goals import display_goals
from src.frontend.rules import display_rules
from src.frontend.tasks import display_tasks

st.set_page_config(page_title='Momentum Tracker', layout='wide')
st.title("🚀 Momentum: Your Productivity Tracker")

ss = services()
op = db.ops()

page = st.sidebar.radio('NAVIGATION', ['Dashboard', 'Goals', 'Tasks', 'Rules Management'])

if page == 'Dashboard':
    display_dashboard()
elif page == "Goals":
    display_goals()
elif page == "Tasks":
    display_tasks()
elif page == "Rules Management":
    display_rules()
