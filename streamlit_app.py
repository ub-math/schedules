import streamlit as st
import glob
import re
from pathlib import Path
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


st.set_page_config(page_title="UB MTH Course Schedule", layout="wide")

st.session_state.selection = None

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
                    "ENROLLTOTAL": "reg",
                    "SECTIONCAPACITY": "cap",
                    "INSTRUCTIONMODE": "mode",
                   },
                   axis=1
                  )

    df = df[df["course_num"].str.split(" ").str[0].isin(["MTH", "ULC"])]
    df.loc[df["faculty email"].str.startswith("None"), "faculty email"] = "Unknown"

    df = df[["course_num",
             "type",
             "course_name",
             "faculty",
             "faculty email",
             "days",
             "start",
             "end",
             "room",
             "reg",
             "cap",
             "mode"
            ]].copy()

    df = df.sort_values(by="course_num")

    return semester, df


fall = "https://blue.math.buffalo.edu/assoc_chair/2239/2239_all_mth_courses.csv"
spring = "https://blue.math.buffalo.edu/assoc_chair/2231/2231_all_mth_courses.csv"


s_fall = process_df(pd.read_csv(fall, sep="\t"))
s_spring = process_df(pd.read_csv(spring, sep="\t"))


dfs = {s[0]: s[1] for s in [s_fall, s_spring]}


st.title("Schedule of MTH Courses")


st.selectbox(
"",
dfs.keys(),
label_visibility="collapsed",
key = "select_semester",
)

#st.header(st.session_state.select_semester)
df = dfs[st.session_state.select_semester]
#df = df.set_index("course_num", drop=True)
#st.dataframe(df)



container = st.container()

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_side_bar()
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_columns(["type", "reg", "cap"], width = 70)
gb.configure_columns(["start", "end", "days"], width = 80)
gb.configure_columns(["room", "mode"], width = 100)
gb.configure_columns(["course_num", "faculty"], width = 140)
gb.configure_columns(["faculty email"], width = 160)
gb.configure_pagination(enabled=False, paginationAutoPageSize=False, paginationPageSize=50)
gridOptions = gb.build()

data = AgGrid(df,
                   gridOptions=gridOptions,
                   enable_enterprise_modules=True,
                   update_mode=GridUpdateMode.SELECTION_CHANGED,
                   height=400
                   )
st.session_state.selection = pd.DataFrame(data["selected_rows"]).iloc[:, 1:]

if len(st.session_state.selection) > 0:
    container.subheader("Selected rows")
    container.dataframe(st.session_state.selection.set_index("course_num", drop=True))
