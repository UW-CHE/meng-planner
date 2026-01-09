import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from importlib import import_module
import meng_options
import ug_specializations
from collections import defaultdict


__all__ = [
    'make_pretty',
    'reset_state',
    'add_header',
    'meng_course_schedule',
    'ug_course_schedule',
    'update_boxes',
    'reset_boxes',
    'set_program_meng',
    'set_start_term_meng',
    'set_program_ug',
    'set_start_term_ug',
    'update_text_field',
    'deactivate_boxes',
    'initialize_defaults',
]


def initialize_defaults():
    init = {
        'meng_program_selectbox.index': 0,
        'meng_start_term_selectbox.index': 5,
        'ug_program_selectbox.index': 0,
        'ug_start_term_selectbox.index': 2,
        'disable': defaultdict(lambda: False),
        'disable_ug': defaultdict(lambda: False),
        'ug_plan': {},
        'meng_plan': {},
        'initialized': True,
    }
    # Initialize session state
    for k, v in init.items():
        if k not in st.session_state.keys():
            st.session_state[k] = v


def ug_course_schedule(start_term='0'):
    with st.expander('Course Schedule', expanded=False):
        dfs = []
        dfs.append(pd.read_csv('./schedules/schedule_500.csv', skipinitialspace=True))
        dfs.append(pd.read_csv('./schedules/schedule_TE.csv', skipinitialspace=True))
        df = pd.concat(dfs, ignore_index=True)
        df.set_index('Course', inplace=True)
        for col in df.keys():  # Remove terms prior to start date
            if col < start_term:
                del df[col]
        st.dataframe(df.style.pipe(make_pretty))
        return df


def meng_course_schedule(start_term='0'):
    with st.expander('Course Schedule', expanded=False):
        incl_seed = st.checkbox('Include SEED Courses')
        incl_hlth = st.checkbox('Include HLTH Courses')
        dfs = []
        dfs.append(pd.read_csv('./schedules/schedule_500.csv', skipinitialspace=True))
        dfs.append(pd.read_csv('./schedules/schedule_600.csv', skipinitialspace=True))
        if incl_hlth:
            dfs.append(pd.read_csv('./schedules/schedule_HLTH.csv', skipinitialspace=True))
        if incl_seed:
            dfs.append(pd.read_csv('./schedules/schedule_SEED.csv', skipinitialspace=True))
        df = pd.concat(dfs, ignore_index=True)
        df.set_index('Course', inplace=True)
        for col in df.keys():  # Remove terms prior to start date
            if col < start_term:
                del df[col]
        st.dataframe(df.style.pipe(make_pretty))
        return df


def make_pretty(styler):
    # styler.hide()
    styler.background_gradient(cmap=plt.cm.PiYG, vmin=-2, vmax=3, axis=None)
    styler.format(precision=0)
    return styler


def reset_state():
    reset_state_meng()
    reset_state_ug()


def set_program_meng(programs):
    options = [p.name for p in programs]
    index = options.index(st.session_state['meng_program_selectbox'])
    st.session_state['meng_program_selectbox.index'] = index
    reset_state_meng()


def set_start_term_meng(terms):
    start = st.session_state['meng_start_term_selectbox']
    index = terms.index(start)
    st.session_state['meng_start_term_selectbox.index'] = index
    st.session_state['meng_plan'].start_term = start


def set_program_ug(programs):
    options = [p.name for p in programs]
    index = options.index(st.session_state['ug_program_selectbox'])
    st.session_state['ug_program_selectbox.index'] = index
    reset_state_ug()


def set_start_term_ug(terms):
    index = terms.index(st.session_state['ug_start_term_selectbox'])
    st.session_state['ug_start_term_selectbox.index'] = index
    reset_state_ug()


def reset_state_meng():
    try:
        st.session_state['meng_plan'].clear()
    except KeyError:
        pass
    reset_boxes()


def reset_state_ug():
    try:
        st.session_state['ug_plan'].clear()
    except KeyError:
        pass
    reset_boxes()


def add_header(term):
    if term.endswith('9'):
        st.markdown("### Fall :maple_leaf:")
    elif term.endswith('5'):
        st.markdown("### Spring :sunflower:")
    elif term.endswith('1'):
        st.markdown("### Winter :snowflake:")
    st.markdown(f"**Term: {term}**")


def get_meng_programs():
    programs = []
    for n in dir(meng_options):
        if not n.startswith('_'):
            globals()[n] = getattr(import_module('meng_options'), n)
            programs.append(globals()[n])
    programs = [p for p in programs if p.name]
    return programs


def get_ug_specializations():
    programs = []
    for n in dir(ug_specializations):
        if not n.startswith('_'):
            globals()[n] = getattr(import_module('ug_specializations'), n)
            programs.append(globals()[n])
    programs = [p for p in programs if p.name]
    return programs


def reset_boxes():
    for item in st.session_state.keys():
        if item.startswith('box_'):
            st.session_state[item] = False
            st.session_state['disable'][item] = False
    _ = st.session_state.pop('df_meng', None)
    _ = st.session_state.pop('df_ug', None)


def deactivate_boxes(term, course):
    key = 'box_'+term+course
    for item in st.session_state.keys():
        if item.startswith('box_') and item.endswith(course) and (item != key):
            if key in st.session_state.keys():
                st.session_state['disable_ug'][item] = st.session_state[key]
                st.session_state['disable'][item] = st.session_state[key]
            else:
                st.session_state['disable_ug'][item] = False
                st.session_state['disable'][item] = False


def update_boxes(term, course, plan):
    key = 'box_'+term+course
    if st.session_state[key] is True:
        st.session_state[plan][course] = term
    else:
        _ = st.session_state[plan].pop(course, None)
    deactivate_boxes(term, course)


def update_text_field(key, plan):
    course = st.session_state[key]
    term = key.split('_')[1]
    old_value = st.session_state[f'{key}.cache']
    if course == '':
        _ = st.session_state[plan].pop(old_value, None)
    elif course != old_value:
        _ = st.session_state[plan].pop(old_value, None)
        st.session_state[plan][course] = term
    elif course not in st.session_state[plan]:
        st.session_state[plan][course] = term
    st.session_state[f'{key}.cache'] = course
