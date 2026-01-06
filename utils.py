import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


__all__ = [
    'make_pretty',
    'reset_state',
    'add_header'
    'meng_course_selector',
    'ug_course_selector'
]


def ug_course_selector():
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
        st.dataframe(df.style.pipe(make_pretty))
        return df


def meng_course_selector(plan):
    with st.expander('Course Schedule', expanded=False):
        incl_earth = st.checkbox('Include EARTH Courses')
        incl_seed = st.checkbox('Include SEED Courses', value="Sustainable" in plan.name)
        incl_hlth = st.checkbox('Include HLTH Courses', value='Health Tech' in plan.name)
        dfs = []
        dfs.append(pd.read_csv('./schedules/schedule_500.csv', skipinitialspace=True))
        dfs.append(pd.read_csv('./schedules/schedule_600.csv', skipinitialspace=True))
        if incl_earth:
            dfs.append(pd.read_csv('./schedules/schedule_EARTH.csv', skipinitialspace=True))
        if incl_hlth:
            dfs.append(pd.read_csv('./schedules/schedule_HLTH.csv', skipinitialspace=True))
        if incl_seed:
            dfs.append(pd.read_csv('./schedules/schedule_SEED.csv', skipinitialspace=True))
        df = pd.concat(dfs, ignore_index=True)
        df.set_index('Course', inplace=True)
        for col in df.keys():  # Remove terms prior to start date
            if col < plan.start_term:
                del df[col]
        st.dataframe(df.style.pipe(make_pretty))
        return df


def make_pretty(styler):
    # styler.hide()
    styler.background_gradient(cmap=plt.cm.PiYG, vmin=-2, vmax=3, axis=None)
    styler.format(precision=0)
    return styler


def reset_state():
    for k in st.session_state.keys():
        if k.startswith('checkbox'):
            st.session_state[k] = False
    # reset_state_meng()
    # reset_state_ug()


def reset_state_meng():
    try:
        st.session_state['plan'].clear()
    except KeyError:
        pass


def reset_state_ug():
    try:
        st.session_state['ug_plan'].clear()
    except KeyError:
        pass


def add_header(term):
    if term.endswith('9'):
        st.header("Fall :maple_leaf:")
    elif term.endswith('5'):
        st.header("Spring :sunflower:")
    elif term.endswith('1'):
        st.header("Winter :snowflake:")
    st.markdown(f"**Term: {term}**")
