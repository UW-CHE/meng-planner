import streamlit as st
from utils import initialize_defaults

if 'initialized' not in st.session_state.keys():
    initialize_defaults()

pg = st.navigation([
    st.Page("pages/0_Home.py"), 
    st.Page("pages/1_MEng_Planner.py"), 
    st.Page("pages/2_UG_Specialization.py")
])

pg.run()
