import streamlit as st
from utils import initialize_defaults

if 'initialized' not in st.session_state.keys():
    initialize_defaults()

st.title("UW CHE MEng Planner")
st.markdown("### Welcome to the the planning tool")
instructions = r"""
This tool can help you choose which courses to take during each
term so that you can earn a desired specialization. This is
accessed through the **MEng Planner** link in the side bar.

If you did your undergrad degree at UW, this tool also helps
to ensure that you take the correct courses during your undergrad
so that the necessary courses are available to take during your 
MEng program. This information is entered through the 
**UG Specialization** link in the side bar.
"""
st.markdown(instructions)

