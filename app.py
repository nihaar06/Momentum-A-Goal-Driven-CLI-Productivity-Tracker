import streamlit as st
import pandas as pd
import plotly.express as px
from db import ops
from services import services
from dashboard import display_dashboard
from goals import display_goals
from rules import display_rules
from tasks import display_tasks

st.set_page_config(page_title='Momentum Tracker',layout='wide')
st.title("🚀 Momentum: Your Productivity Tracker")

ss=services()
op=ops()

page=st.sidebar.radio('NAVIGATION',['Dashboard','Goals','Tasks','Rules Management'])
if page=='Dashboard':
    display_dashboard()
elif page == "Goals":
    display_goals()
elif page == "Tasks":
    display_tasks()
elif page == "Rules Management":
    display_rules()