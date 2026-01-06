import streamlit as st
import pandas as pd
import numpy as np
from importlib import import_module
from utils import (
    make_pretty,
    reset_state_ug,
    reset_state,
    add_header,
    ug_course_schedule,
)
import ug_specializations


st.title(":calendar: UG Specialization Planner")
st.set_page_config(layout="wide")

# Import all options into list of programs
programs = []
for n in dir(ug_specializations):
    if not n.startswith('_'):
        globals()[n] = getattr(import_module('ug_specializations'), n)
        programs.append(globals()[n])
# Generate selectbox of programs
program_name = st.sidebar.selectbox(
    label='Choose Specialization', 
    options=[p.name for p in programs if p.name], 
    # on_change=reset_state_ug,
)
# Extract selected program
program = [p for p in programs if p.name == program_name]
plan = program[0]()  # Instantiate plan object
st.session_state['ug_plan'] = plan  # Store plan in state


terms = ['1' + f"{25+i}" + j for i in range(6) for j in ['1', '5', '9']]
# Retrieve start term from selectbox
plan.start_term = st.sidebar.selectbox(
    label='Select Start Term', 
    options=terms, 
    index=5, 
    # on_change=reset_state_ug,
)

# Add a reset button to side bar
if st.sidebar.button('Reset'):
    reset_state()

# Generate the upcoming roster of classes and show in a table
df = ug_course_schedule()

# Generate the columns for each term
start_j = terms.index(plan.start_term)
cols = st.columns(len(plan.max_per_term))
i = 1000  # This is used to generate a unique key for each checkbox
for j, col in enumerate(cols):
    term = terms[start_j + j]
    plan[term] = []
    with col:
        add_header(term)
        with st.container(border=True):
            for item in df.index:
                if (df.loc[item][term]) and (item not in plan.prescribed_courses):
                    if item in plan.courses:
                        st.checkbox(item, key=f'checkbox_{i}', value=True, disabled=True)
                    else:
                        if st.checkbox(item, value=False, key=f'checkbox_{i}'):
                            plan[term].append(item)
                    i += 1

# Check to ensure no problems are found with selections
overload = np.array(plan.count_per_term) > np.array(plan.max_per_term)
if np.any(overload):
    i = np.where(overload)[0][0]
    st.error(f'No more than {plan.max_per_term[i]} courses may be taken in term {i+1}')
else:  # Count the number of courses and generate progress bars and messages
    pcol1 = st.columns(2)
    if len(plan.required) >= 0:
        with pcol1[0]:
            pbar1 = st.progress(0)
            N = 4
            pbar1.progress(min(N, len(plan.courses))/N)
        with pcol1[1]:
            if (len(plan.courses) >= 4):
                st.success('Specialization achieved!')
            else:
                st.error('Specialization requirements not met')
