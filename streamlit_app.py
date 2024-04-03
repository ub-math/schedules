import streamlit as st
import glob
import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

from plots import plot_schedule


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


    df = df[df["course_num"].str.split(" ").str[0].isin(["MTH", "ULC", "CDA"])]
    df["course_num"] = df["course_num"].str.extract(r"([A-Z]{3} \d{3})[^ ]+(.*)").sum(axis=1)
    df = df[df["type"] != "TUT"]
    df.loc[df["faculty email"].str.startswith("None"), "faculty email"] = "Unknown"
    df["faculty"] = df["faculty"].str.extract(r"([A-Za-z]+)[^,]*(,\s*[A-Za-z]+)?").fillna("").sum(axis=1)



    non_MTH = (~df["course_num"].str.match(r"MTH.*")) | df["course_num"].str.match(r"MTH\s+(112|113|114).*")
    df["prefix"] = df["course_num"].str.extract(r"^(.+?)[1-9]?$")
    df.loc[non_MTH, "prefix"] =  df.loc[non_MTH, "course_num"]


    def add_lecturer(g):
        if "LEC" in g["type"].values:
            lecturer = g[g["type"] == "LEC"]["lecturer"].iloc[0]
            g['lecturer'] = lecturer
        return g

    df["lecturer"] = df["faculty"]
    df = df.groupby(by="prefix", group_keys=False).apply(add_lecturer, include_groups = False)


    df = df[["course_num",
            "type",
            "course_name",
            "faculty",
            "faculty email",
            "lecturer",
            "days",
            "start",
            "end",
            "room",
            "reg",
            "cap",
            "mode",
        ]].copy()

    df = df.sort_values(by="course_num")

    return semester, df



summer = "https://blue2021.math.buffalo.edu/assoc_chair/2246/2246_all_mth_courses.csv"
fall = "https://blue2021.math.buffalo.edu/assoc_chair/2249/2249_all_mth_courses.csv"
winter = "https://blue2021.math.buffalo.edu/assoc_chair/2240/2240_all_mth_courses.csv"
spring = "https://blue2021.math.buffalo.edu/assoc_chair/2241/2241_all_mth_courses.csv"



s_summer = process_df(pd.read_csv(summer, sep="\t"))
s_fall = process_df(pd.read_csv(fall, sep="\t"))
s_winter = process_df(pd.read_csv(winter, sep="\t"))
s_spring = process_df(pd.read_csv(spring, sep="\t"))

dfs = {s[0]: s[1] for s in [s_winter, s_spring, s_summer, s_fall]}


st.title("Schedule of MTH Courses")

col1, col2 = st.columns([1, 3])

col1.selectbox("hidden",
               dfs.keys(),
               index=1,
               label_visibility="collapsed",
               key = "select_semester"
               )

st.header(st.session_state.select_semester)
df = dfs[st.session_state.select_semester]
#df = df.set_index("course_num", drop=True)
#st.dataframe(df)

print(df)


container = st.container()
ccol1, ccol2, ccol3, = container.columns([1, 1, 1])

st.markdown("**Note.** The `lecturer` column lists the course lecturer - the same for lectures and all associated recitation of the course.")
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_side_bar()
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_columns(["type", "reg", "cap"], width = 70)
gb.configure_columns(["start", "end", "days"], width = 80)
gb.configure_columns(["room", "mode"], width = 100)
gb.configure_columns(["course_num"], width = 160)
gb.configure_columns(["faculty", "lecturer"], width = 120)
gb.configure_columns(["faculty email"], width = 160)
gb.configure_grid_options(enableRangeSelection=True,
                          enableRangeHandle=True,
                          )
gridOptions = gb.build()

data = AgGrid(df,
              gridOptions=gridOptions,
              enable_enterprise_modules=True,
              update_mode=GridUpdateMode.SELECTION_CHANGED,
              #height=400
             )
st.session_state.selection = pd.DataFrame(data["selected_rows"]).iloc[:, 1:]


st.session_state.selection_plot = plt.figure()

def make_plot():

    st.session_state["selection_plot"] = plot_schedule(st.session_state.selection)
    ccol2.pyplot(st.session_state.selection_plot)

if len(st.session_state.selection) > 0:
    container.subheader("Selected rows")
    container.dataframe(st.session_state.selection.set_index("course_num", drop=True))
    container.button("Plot selection", on_click = make_plot)
