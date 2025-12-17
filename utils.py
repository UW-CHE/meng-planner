import matplotlib.pyplot as plt
import streamlit as st


__all__ = [
    'make_pretty',
    'reset_state',
    'add_header'
]


def make_pretty(styler):
    # styler.hide()
    styler.background_gradient(cmap=plt.cm.PiYG, vmin=-2, vmax=3, axis=None)
    styler.format(precision=0)
    return styler


def reset_state():
    for k in st.session_state.keys():
        if k.startswith('checkbox'):
            st.session_state[k] = False
    st.session_state['plan'].clear()


def add_header(term):
    if term.endswith('9'):
        st.header(f"Fall :maple_leaf:")
    elif term.endswith('5'):
        st.header(f"Spring :sunflower:")
    elif term.endswith('1'):
        st.header(f"Winter :snowflake:")
    st.markdown(f"**Term: {term}**")
