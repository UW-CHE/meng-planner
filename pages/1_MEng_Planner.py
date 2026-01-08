from collections import defaultdict
import streamlit as st
import pandas as pd
import numpy as np
from utils import (
    reset_state_meng,
    add_header,
    meng_course_schedule,
    get_meng_programs,
    update_boxes,
    reset_boxes,
    set_start_term_meng,
    set_program_meng,
    update_text_field,
    deactivate_boxes,
)

init = {
    'meng_program_selectbox.index': 0,
    'meng_start_term_selectbox.index': 5,
}

# Initialize session state
for k, v in init.items():
    if k not in st.session_state.keys():
        st.session_state[k] = v

st.set_page_config(
    page_title="MEng Planner",
    page_icon=":calendar:",
)
st.title(":calendar: MEng Planner")
st.set_page_config(layout="wide")

# Generate list of available programs
programs = get_meng_programs()

# Populate sidebar with some dropdown boxes
st.sidebar.selectbox(
    label='Choose Program', 
    options=[p.name for p in programs], 
    key='meng_program_selectbox',
    on_change=set_program_meng,
    args=(programs,),
    index=st.session_state['meng_program_selectbox.index']
)
program_name = st.session_state['meng_program_selectbox']
if ('meng_plan' not in st.session_state.keys()) or (len(st.session_state['meng_plan']) == 0):
    program = [p for p in programs if p.name == program_name]
    plan = program[0]()
    st.session_state['meng_plan'] = plan  # Store plan in state
    st.session_state['disable'] = defaultdict(lambda: False)

# Deal with starting term by generating a long list of future term numbers
terms = ['1' + f"{25+i}" + j for i in range(6) for j in ['1', '5', '9']]
# Retrieve start term from selectbox
st.session_state['meng_plan'].start_term = st.sidebar.selectbox(
    label='Select Start Term',
    options=terms,
    on_change=set_start_term_meng,
    args=(terms,),
    key='meng_start_term_selectbox',
    index=st.session_state['meng_start_term_selectbox.index'],
)

# Add a reset button to side bar
if st.sidebar.button('Reset'):
    reset_state_meng()
    reset_boxes()

# Generate the upcoming roster of classes and show in a table
df_meng = meng_course_schedule(st.session_state['meng_plan'].start_term)
df_meng = df_meng.iloc[:, :st.session_state['meng_plan'].N_terms]

cols = st.columns(st.session_state['meng_plan'].N_terms)
cols = {term: cols[i] for i, term in enumerate(df_meng.keys())}
for i, term in enumerate(cols.keys()):
    with cols[term]:
        add_header(term)
        for course in df_meng.index[df_meng[term] == 1]:
            mark = ' :star:' if course in st.session_state['meng_plan'].prescribed_courses else ''
            key = 'box_'+term+course
            # I think key needs to include meng and ug so they don't interfere
            # This applies to the disable flag especially
            label = course+mark
            value = st.session_state['meng_plan'][course] == term
            if st.session_state['meng_plan'].max_per_term[i] == 0:
                st.session_state['disable'][key] = True
            st.checkbox(
                label=label,
                key=key,
                on_change=update_boxes,
                args=(term, course, 'meng_plan'),
                disabled=st.session_state['disable'][key],
                value=value,
            )
        # Add custom courses
        if 'text_'+term+'custom.cache' not in st.session_state.keys():
            st.session_state['text_'+term+'custom.cache'] = ''
        value = st.session_state['text_'+term+'custom.cache']
        st.text_input(
            label='Custom',
            key='text_'+term+'custom',
            value=value,
            on_change=update_text_field,
            args=(term, 'meng_plan'),
            width=100,
            label_visibility='collapsed',
            placeholder='Custom',
        )

st.sidebar.divider()
with st.sidebar.expander('Show MEng plan', expanded=True):
    st.write('Course : Term')
    st.write(st.session_state['meng_plan'])

# Check to ensure no problems are found with selections
overload = st.session_state['meng_plan'].overloaded_terms()
if np.any(overload):
    i = np.where(overload)[0][0]
    st.error(f'No more than {st.session_state['meng_plan'].max_per_term[i]} courses may be taken in term {i+1}')
elif st.session_state['meng_plan'].count_500s() > st.session_state['meng_plan'].N_required // 3:
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
