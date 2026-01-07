import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from importlib import import_module
import meng_options
import ug_specializations


__all__ = [
    'make_pretty',
    'reset_state',
    'add_header'
    'meng_course_schedule',
    'ug_course_schedule'
]


def ug_course_schedule(start_term='0'):
    with st.expander('Course Schedule', expanded=False):
        incl_mme = st.checkbox('Include MME Courses')
        incl_earth = st.checkbox('Include EARTH Courses')
        dfs = []
        dfs.append(pd.read_csv('./schedules/schedule_500.csv', skipinitialspace=True))
        if incl_mme:
            dfs.append(pd.read_csv('./schedules/schedule_MME.csv', skipinitialspace=True))
        if incl_earth:
            dfs.append(pd.read_csv('./schedules/schedule_EARTH.csv', skipinitialspace=True))
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


def reset_state_meng():
    try:
        st.session_state['meng_plan'].clear()
    except KeyError:
        pass
    reset_courses()


def reset_state_ug():
    try:
        st.session_state['ug_plan'].clear()
    except KeyError:
        pass
    reset_courses()


def add_header(term):
    if term.endswith('9'):
        st.header("Fall :maple_leaf:")
    elif term.endswith('5'):
        st.header("Spring :sunflower:")
    elif term.endswith('1'):
        st.header("Winter :snowflake:")
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


def reset_courses():
    for item in st.session_state.keys():
        if item.startswith('box_'):
            st.session_state[item] = False
    try:
        del st.session_state['df_meng']
        del st.session_state['df_ug']
    except:
        pass
