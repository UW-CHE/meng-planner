import streamlit as st
import pandas as pd
from planner import (
    Specialization,
    make_pretty,
)


class AccelMEngMLAI(Specialization):
    name = 'Accel MEng in AI/ML'
    Nterms = 4
    Nrequired = 8
    mandatory = ['CHE523', 'CHE626']
    optional = ['CHE520', 'CHE521', 'CHE522', 'CHE621', 'CHE620']


class MEngMLAI(Specialization):
    name = 'MEng in AI/ML'
    Nterms = 3
    Nrequired = 8
    mandatory = ['CHE523', 'CHE626']
    optional = ['CHE520', 'CHE521', 'CHE522', 'CHE621', 'CHE620']


class MEng(Specialization):
    name = 'MEng'
    Nterms = 3
    Nrequired = 8
    mandatory = []
    optional = []


class AccelMEngSEAM(Specialization):
    name = 'Accel MEng in Sustainable Energy & Materials'
    Nterms = 4
    Nrequired = 8
    mandatory = ['SEED671', 'SEED672']
    optional = ['CHE571', 'CHE572', 'CHE514', 'CHE602']


def reset_state():
    for k in st.session_state.keys():
        if k.startswith('checkbox'):
            st.session_state[k] = False
    courses.clear()

st.title(":calendar: MEng Planner")
st.set_page_config(layout="wide")

programs = (AccelMEngMLAI, AccelMEngSEAM, MEngMLAI, MEng)
program_name = st.sidebar.selectbox('Choose Program', options=[p.name for p in programs], on_change=reset_state)
program = [p for p in programs if p.name == program_name]
courses = program[0]()

terms = ['1' + f"{25+i}" + j for i in range(6) for j in ['1', '5', '9']]
start_term = st.sidebar.selectbox('Select Start Term', options=terms, index=5)

if st.sidebar.button('Reset'):
    reset_state()

with st.expander('Course Schedule', expanded=False):
    df_500 = pd.read_csv('schedule_500.csv', skipinitialspace=True)
    df_600 = pd.read_csv('schedule_600.csv', skipinitialspace=True)
    df = pd.concat([df_500, df_600], ignore_index=True)
    df.set_index('Course', inplace=True)
    st.dataframe(df.style.pipe(make_pretty))

start_j = terms.index(start_term)
cols = st.columns(courses.Nterms)
term_count = {}
i = 0
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
if any([c > 3 for c in term_count.values()]):
    st.error('No more than 3 courses may be taken each term')
elif courses.count_500s() > 2:
    st.error('No more than 2 500-level courses are allowed')
elif courses.count_nonCHE() > 2:
    st.error('No more than 2 courses can be from outside CHE (or NANO)')
else:
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
