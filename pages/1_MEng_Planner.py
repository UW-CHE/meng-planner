import streamlit as st
import pandas as pd
import numpy as np
from importlib import import_module
from utils import (
    make_pretty,
    reset_state_meng,
    reset_state,
    add_header,
    meng_course_selector,
)
import meng_options

st.set_page_config(
    page_title="MEng Planner",
    page_icon=":calendar:",
)

st.title(":calendar: MEng Planner")
st.set_page_config(layout="wide")

# Import all options into list of programs
programs = []
for n in dir(meng_options):
    if not n.startswith('_'):
        globals()[n] = getattr(import_module('meng_options'), n)
        programs.append(globals()[n])

cols = st.sidebar.columns((0.6, 0.4), vertical_alignment='bottom')
with cols[0]:  # Generate selectbox of programs
    program_name = st.selectbox(
        label='Choose Program', 
        options=[p.name for p in programs if p.name], 
        # on_change=reset_state_meng,
    )
with cols[1]:  # Apply selected program
    if st.button('Apply'):
        program = [p for p in programs if p.name == program_name]
        plan = program[0]()
        st.session_state['plan'] = plan  # Store plan in state
    else:
        try:
            plan = st.session_state['plan'] 
        except KeyError:
            pass

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

# Generate the upcoming roster of classes and show in a table
df = meng_course_selector(plan)

# Add UG courses to list of ineligible
try:
    plan.ineligible = st.session_state['ug_plan'].courses
except KeyError:
    plan.ineligible = []

# Generate the columns for each term
start_j = terms.index(plan.start_term)
cols = st.columns(len(plan.max_per_term))
i = 0  # This is used to generate a unique key for each checkbox
for j, col in enumerate(cols):
    term = terms[start_j + j]
    plan[term] = []
    with col:
        add_header(term)
        with st.container(border=True):
            if plan.max_per_term[j] == 0:
                st.write("This is a coop term")
            else:
                # Add specialization courses to column
                if len(plan.required) > 0:
                    st.markdown('*Specialization Courses*')
                    for item in plan.prescribed_courses:
                        if df.loc[item][term]:
                            if item in plan.courses:
                                st.checkbox(item, key=f'checkbox_{i}', value=True, disabled=True)
                            elif item in plan.ineligible:
                                st.checkbox(item, key=f'checkbox_{i}', value=False, disabled=True, help='This is already taken')
                            else:
                                if st.checkbox(item, value=False, key=f'checkbox_{i}'):
                                    plan[term].append(item)
                            i += 1
                    st.divider()
                # Now add remainder of courses
                st.markdown('*General Courses*')
                for item in df.index:
                    if (df.loc[item][term]) and (item not in plan.prescribed_courses):
                        if item in plan.courses:
                            st.checkbox(item, key=f'checkbox_{i}', value=True, disabled=True)
                        elif item in plan.ineligible:
                            st.checkbox(item, key=f'checkbox_{i}', value=False, disabled=True)
                        else:
                            if st.checkbox(item, value=False, key=f'checkbox_{i}'):
                                plan[term].append(item)
                        i += 1

# Check to ensure no problems are found with selections
overload = np.array(plan.count_per_term) > np.array(plan.max_per_term)
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
    if len(plan.required) > 0:
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

if st.checkbox('Show plan'):
    st.write(plan)
