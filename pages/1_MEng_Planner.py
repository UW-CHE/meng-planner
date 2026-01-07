import streamlit as st
import pandas as pd
import numpy as np
from utils import (
    reset_state_meng,
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
    label='Choose MEng Program', 
    options=[p.name for p in programs], 
    on_change=reset_state_meng,
)
if ('meng_plan' not in st.session_state.keys()) or (len(st.session_state['meng_plan']) == 0):
    program = [p for p in programs if p.name == program_name]
    plan = program[0]()
    st.session_state['meng_plan'] = plan  # Store plan in state

# Deal with starting term by generating a long list of future term numbers
terms = ['1' + f"{25+i}" + j for i in range(6) for j in ['1', '5', '9']]
# Retrieve start term from selectbox
st.session_state['meng_plan'].start_term = st.sidebar.selectbox(
    label='Select MEng Start Term',
    options=terms,
    index=5,
    on_change=reset_state_meng,
)

# Add a reset button to side bar
if st.sidebar.button('Reset'):
    reset_state_meng()
    reset_courses()

# Generate the upcoming roster of classes and show in a table
df_meng = meng_course_schedule(st.session_state['meng_plan'].start_term)
df_meng = df_meng.iloc[:, :st.session_state['meng_plan'].N_terms]

cols = st.columns(st.session_state['meng_plan'].N_terms)
cols = {term: cols[i] for i, term in enumerate(df_meng.keys())}
for term in cols.keys():
    with cols[term]:
        add_header(term)
        for course in df_meng.index[df_meng[term] == 1]:
            mark = ' :star:' if course in st.session_state['meng_plan'].prescribed_courses else ''
            key = 'box_'+term+course
            label = course+mark
            if course in st.session_state['meng_plan'].keys() and st.session_state['meng_plan'][course] != term:
                st.session_state[key] = False
                st.checkbox(label=label, key=key, disabled=True)
            else:
                val = st.checkbox(label=label, key=key)
                if val:
                    st.session_state['meng_plan'][course] = term
                else:
                    _ = st.session_state['meng_plan'].pop(course, None)

st.sidebar.divider()
with st.sidebar.expander('Show MEng plan', expanded=True):
    st.write('Course : Term')
    st.write(st.session_state['meng_plan'])

# Check to ensure no problems are found with selections
# overload = st.session_state['meng_plan'].overloaded_terms()
# if np.any(overload):
#     i = np.where(overload)[0][0]
#     st.error(f'No more than {st.session_state['meng_plan'].max_per_term[i]} courses may be taken in term {i+1}')
# el
if st.session_state['meng_plan'].count_500s() > st.session_state['meng_plan'].N_required // 3:
    N = st.session_state['meng_plan'].N_required // 3
    st.error(f'No more than {N} 500-level courses are allowed')
elif st.session_state['meng_plan'].count_nonCHE() > st.session_state['meng_plan'].N_outside:
    N = st.session_state['meng_plan'].N_outside
    st.error(f'No more than {N} courses can be from outside CHE or NANO')
else:  # Count the number of courses and generate progress bars and messages
    if hasattr(st.session_state['meng_plan'], 'specialization_count'):
        pcol1 = st.columns(2, vertical_alignment='center')
        with pcol1[0]:
            pbar1 = st.progress(0)
            N = 4
            pbar1.progress(min(N, st.session_state['meng_plan'].specialization_count())/N)
        with pcol1[1]:
            if st.session_state['meng_plan'].specialization_achieved():
                st.success('Specialization achieved!')
            else:
                st.error('Specialization requirements not met')
    pcol2 = st.columns(2, vertical_alignment='center')
    with pcol2[0]:
        pbar2 = st.progress(0)
        N = st.session_state['meng_plan'].N_required
        pbar2.progress(min(N, len(st.session_state['meng_plan'].courses))/N)
    with pcol2[1]:
        if st.session_state['meng_plan'].degree_achieved():
            st.success('Degree requirements achieved!')
        else:
            st.error('Degree requirements not met')


