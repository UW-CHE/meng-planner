from collections import defaultdict
import streamlit as st
import pandas as pd
import numpy as np
from utils import (
    reset_state_ug,
    reset_boxes,
    update_boxes,
    add_header,
    ug_course_schedule,
    get_ug_specializations,
    set_program_ug,
    set_start_term_ug,
)

init = {
    'ug_program_selectbox.index': 0,
    'ug_start_term_selectbox.index': 2,
}

# Initialize session state
for k, v in init.items():
    if k not in st.session_state.keys():
        st.session_state[k] = v

st.set_page_config(
    page_title="UG Specialization Planner",
    page_icon=":calendar:",
)
st.title(":calendar: UG Specialization Planner")
st.set_page_config(layout="wide")

# Generate list of available programs
programs = get_ug_specializations()

# Populate sidebar with some dropdown boxes
st.sidebar.selectbox(
    label='Choose Program', 
    options=[p.name for p in programs], 
    key='ug_program_selectbox',
    on_change=set_program_ug,
    args=(programs,),
    index=st.session_state['ug_program_selectbox.index']
)
program_name = st.session_state['ug_program_selectbox']
if ('ug_plan' not in st.session_state.keys()) or (len(st.session_state['ug_plan']) == 0):
    program = [p for p in programs if p.name == program_name]
    plan = program[0]()
    st.session_state['ug_plan'] = plan  # Store plan in state
    st.session_state['disable'] = defaultdict(lambda: False)

# Deal with starting term by generating a long list of future term numbers
terms = ['1' + f"{25+i}" + j for i in range(6) for j in ['1', '5', '9']]
# Retrieve start term from selectbox
st.session_state['ug_plan'].start_term = st.sidebar.selectbox(
    label='Select Start Term',
    options=terms,
    on_change=set_start_term_ug,
    args=(terms,),
    key='ug_start_term_selectbox',
    index=st.session_state['ug_start_term_selectbox.index'],
)

# Add a reset button to side bar
if st.sidebar.button('Reset'):
    reset_state_ug()
    reset_boxes()

# Generate the upcoming roster of classes and show in a table
df_ug = ug_course_schedule(st.session_state['ug_plan'].start_term)
df_ug = df_ug.iloc[:, :st.session_state['ug_plan'].N_terms]

cols = st.columns(st.session_state['ug_plan'].N_terms)
cols = {term: cols[i] for i, term in enumerate(df_ug.keys())}
for term in cols.keys():
    with cols[term]:
        add_header(term)
        for course in df_ug.index[df_ug[term] == 1]:
            mark = ' :star:' if course in st.session_state['ug_plan'].prescribed_courses else ''
            key = 'box_'+term+course
            label = course+mark
            value = st.session_state['meng_plan'][course] == term
            st.checkbox(
                label=label, 
                key=key, 
                on_change=update_boxes, 
                args=(term, course, 'ug_plan'), 
                disabled=st.session_state['disable'][key],
                value=value,
            )

st.sidebar.divider()
with st.sidebar.expander('Show UG plan', expanded=True):
    st.write('Course : Term')
    st.write(st.session_state['ug_plan'])

pcol1 = st.columns(2, vertical_alignment='center')
with pcol1[0]:
    pbar1 = st.progress(0)
    N = 4
    pbar1.progress(min(N, st.session_state['ug_plan'].specialization_count())/N)
with pcol1[1]:
    if st.session_state['ug_plan'].specialization_achieved():
        st.success('Specialization achieved!')
    else:
        st.error('Specialization requirements not met')
