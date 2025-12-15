import streamlit as st
import pandas as pd
from importlib import import_module
from planner import (
    make_pretty,
)
import options


def reset_state():
    for k in st.session_state.keys():
        if k.startswith('checkbox'):
            st.session_state[k] = False
    courses.clear()

st.title(":calendar: MEng Planner")
st.set_page_config(layout="wide")

# Import all classes in options into list of programs
programs = []
for n in dir(options):
    if not n.startswith('_'):
        globals()[n] = getattr(import_module('options'), n)
        programs.append(globals()[n])
# Generate selectbox of programs
program_name = st.sidebar.selectbox('Choose Program', 
                                    options=[p.name for p in programs if p.name], 
                                    on_change=reset_state,
                                    )
# Extract selected program
program = [p for p in programs if p.name == program_name]
# Instantiate program class
courses = program[0]()

# Deal with starting term by generating a long list of future term numbers
terms = ['1' + f"{25+i}" + j for i in range(6) for j in ['1', '5', '9']]
# Retrieve start term from selectox
start_term = st.sidebar.selectbox('Select Start Term', options=terms, index=5)

# Add a reset button to side bar
if st.sidebar.button('Reset'):
    reset_state()

# Generate the upcoming roster of classes and show in a table
with st.expander('Course Schedule', expanded=False):
    st.markdown('1**25**9 refers to 2025 and 125**9** refers to Sept')
    df_500 = pd.read_csv('schedule_500.csv', skipinitialspace=True)
    df_600 = pd.read_csv('schedule_600.csv', skipinitialspace=True)
    df = pd.concat([df_500, df_600], ignore_index=True)
    df.set_index('Course', inplace=True)
    st.dataframe(df.style.pipe(make_pretty))

# Generate the columns for each term
start_j = terms.index(start_term)
cols = st.columns(len(courses.N_per_term))
term_count = {}
i = 0  # This is used to generate a unique key for each checkbox
for j, col in enumerate(cols):
    term = terms[start_j + j]
    term_count[term] = 0
    with col:
        if term.endswith('9'):
            st.header(f"Fall :maple_leaf:")
        elif term.endswith('5'):
            st.header(f"Spring :sunflower:")
        elif term.endswith('1'):
            st.header(f"Winter :snowflake:")
        st.markdown(f"**Term: {term}**")
        with st.container(border=True):
            # Add specialization specific courses to column
            for item in courses.courses:
                if df.loc[item][term]:
                    if courses[item]:
                        st.checkbox(item, key=f'checkbox_{i}', value=True, disabled=True)
                    else:
                        courses[item] = st.checkbox(item, value=False, key=f'checkbox_{i}')
                        if courses[item]: 
                            term_count[term] += 1
                    i += 1
            st.divider()
            # Now add remainder of courses
            st.markdown('*General Courses*')
            for item in df.index:
                if (df.loc[item][term]) and (item not in courses.courses):
                    if courses[item]:
                        st.checkbox(item, key=f'checkbox_{i}', value=True, disabled=True)
                    else:
                        courses[item] = st.checkbox(item, value=False, key=f'checkbox_{i}')
                        if courses[item]: 
                            term_count[term] += 1
                    i += 1
# Check to ensure no problems are found with selections
for i, N in enumerate(term_count.values()):
    if N > courses.N_per_term[i]:
        st.error(f'No more than {N} courses may be taken in term {i}')
if courses.count_500s() > 2:
    st.error('No more than 2 500-level courses are allowed')
elif courses.count_nonCHE() > 2:
    st.error('No more than 2 courses can be from outside CHE (or NANO)')
else:  # Count the number of courses and generate progress bars and messages
    pcol1 = st.columns(2)
    if len(courses.mandatory) > 0:
        with pcol1[0]:
            pbar1 = st.progress(0)
            N = 4
            pbar1.progress(min(N, courses.specialization_count())/N)
        with pcol1[1]:
            if courses.specialization_achieved():
                st.success('Specialization achieved!')
            else:
                st.error('Specialization requirements not met')
    pcol2 = st.columns(2)
    with pcol2[0]:
        pbar2 = st.progress(0)
        N = courses.Nrequired
        pbar2.progress(min(N, sum(courses.values()))/N)
    with pcol2[1]:
        if courses.degree_achieved():
            st.success('Degree requirements achieved!')
        else:
            st.error('Degree requirements not met')
