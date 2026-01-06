import streamlit as st
import pandas as pd
import numpy as np
from utils import (
    reset_state,
    reset_courses,
    add_header,
    meng_course_schedule,
    get_meng_programs,
)


st.set_page_config(
    page_title="MEng Planner",
    page_icon=":calendar:",
)
st.title(":calendar: MEng Planner")
st.set_page_config(layout="wide")

# Generate list of available programs
programs = get_meng_programs()

# Populate sidebar with some dropdown boxes
program_name = st.sidebar.selectbox(
    label='Choose Program', 
    options=[p.name for p in programs], 
    # on_change=reset_state_meng,
)
program = [p for p in programs if p.name == program_name]
plan = program[0]()
st.session_state['plan'] = plan  # Store plan in state

# Deal with starting term by generating a long list of future term numbers
terms = ['1' + f"{25+i}" + j for i in range(6) for j in ['1', '5', '9']]
# Retrieve start term from selectbox
plan.start_term = st.sidebar.selectbox(
    label='Select Start Term',
    options=terms,
    index=5,
    # on_change=reset_state_meng,
)

# Add a reset button to side bar
if st.sidebar.button('Reset'):
    reset_state()
    reset_courses()

# Generate the upcoming roster of classes and show in a table
df_offered = meng_course_schedule(plan.start_term)
df_taken = df_offered.copy()
df_taken = df_taken.iloc[:, :4]
df_taken.iloc[:] = False
st.session_state['df_taken'] = df_taken

cols = st.columns(len(st.session_state['df_taken'].keys()))
cols = {term: cols[i] for i, term in enumerate(st.session_state['df_taken'].keys())}
for term in st.session_state['df_taken'].keys():
    with cols[term]:
        add_header(term)
        for course in df_offered.index[df_offered[term] == 1]:
            mark = ' :star:' if course in plan.prescribed_courses else ''
            key = 'box_'+term+course
            label = course+mark
            disabled = st.session_state['df_taken'].loc[course].sum() > 0
            if disabled:  # Turn off box and set it to unchecked
                st.session_state[key] = False
                st.checkbox(label=label, key=key, disabled=True)
            else:
                val = st.checkbox(label=label, key=key)
                st.session_state['df_taken'][term].loc[course] = val
                if val:
                    plan[course] = term

# st.write(st.session_state['df_taken'])
st.sidebar.divider()
with st.sidebar.expander('Show plan'):
    st.write('Course : Term')
    st.write(plan)

# Check to ensure no problems are found with selections
overload = st.session_state['df_taken'].sum(axis=0) > np.array(plan.max_per_term)
if np.any(overload):
    i = np.where(overload)[0][0]
    st.error(f'No more than {plan.max_per_term[i]} courses may be taken in term {i+1}')
elif plan.count_500s() > plan.N_required // 3:
    N = plan.N_required // 3
    st.error(f'No more than {N} 500-level courses are allowed')
elif plan.count_nonCHE() > plan.N_outside:
    N = plan.N_outside
    st.error(f'No more than {N} courses can be from outside CHE or NANO')
else:  # Count the number of courses and generate progress bars and messages
    pcol1 = st.columns(2, vertical_alignment='center')
    with pcol1[0]:
        pbar1 = st.progress(0)
        N = 4
        pbar1.progress(min(N, plan.specialization_count())/N)
    with pcol1[1]:
        if plan.specialization_achieved():
            st.success('Specialization achieved!')
        else:
            st.error('Specialization requirements not met')
    pcol2 = st.columns(2, vertical_alignment='center')
    with pcol2[0]:
        pbar2 = st.progress(0)
        N = plan.N_required
        pbar2.progress(min(N, len(plan.courses))/N)
    with pcol2[1]:
        if plan.degree_achieved():
            st.success('Degree requirements achieved!')
        else:
            st.error('Degree requirements not met')


