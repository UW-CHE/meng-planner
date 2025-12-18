import streamlit as st
import pandas as pd
import numpy as np
from importlib import import_module
from utils import (
    make_pretty,
    reset_state,
    add_header,
)
import options


st.title(":calendar: UG Specialization Planner")
st.set_page_config(layout="wide")

