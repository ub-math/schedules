import streamlit as st
import glob
import re
from pathlib import Path
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(layout="wide")


def process_df(df):

    semester = df.iat[0, 1]

    df = df.rename({"CLASSNUMBERSECTION": "course_num",
                    "COURSETYPESOURCEKEY": "type",
                    "COURSEDESCRIPTION": "course_name",
                    "FACULTY": "faculty",
                    "faculty email": "faculty email",
                    "CLASSMEETINGPATTERNSOURCEKEY": "days",
                    "CLASSSTARTTIME": "start",
                    "CLASSENDTIME": "end",
                    "ROOM": "room",
                    "ENROLLTOTAL": "enrollment",
                    "SECTIONCAPACITY": "capacity",
                    "INSTRUCTIONMODE": "mode",
                   },
                   axis=1
                  )

    df = df[["course_num",
             "type",
             "course_name",
             "faculty",
             "faculty email",
             "days",
             "start",
             "end",
             "room",
             "enrollment",
             "capacity",
             "mode"
            ]].copy()



    return semester, df


fall = "https://blue.math.buffalo.edu/assoc_chair/2239/2239_all_mth_courses.csv"
spring = "https://blue.math.buffalo.edu/assoc_chair/2231/2231_all_mth_courses.csv"


s_fall = process_df(pd.read_csv(fall, sep="\t"))
s_spring = process_df(pd.read_csv(spring, sep="\t"))


dfs = {s[0]: s[1] for s in [s_fall, s_spring]}

"""
with st.sidebar:

    st.header("Semester")

    st.selectbox(
    "",
    dfs.keys(),
    label_visibility="collapsed",
    key = "select_semester",
    )


    with st.form("search_form"):
        st.write("hello")


        submitted = st.form_submit_button("Submit")
"""


st.header("Semester")

st.selectbox(
"",
dfs.keys(),
label_visibility="collapsed",
key = "select_semester",
)

st.header(st.session_state.select_semester)
df = dfs[st.session_state.select_semester]
#df = df.set_index("course_num", drop=True)
st.dataframe(df)


AgGrid(df,  fit_columns_on_grid_load=False)
