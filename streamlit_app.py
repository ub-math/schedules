import streamlit as st
import glob
import re
from pathlib import Path
import pandas as pd

st.set_page_config(layout="wide")

fall = "https://blue.math.buffalo.edu/assoc_chair/2239/2239_all_mth_courses.csv"
spring = "https://blue.math.buffalo.edu/assoc_chair/2231/2231_all_mth_courses.csv"
summer = "https://blue.math.buffalo.edu/assoc_chair/2231/2231_all_mth_courses.csv"


df_fall = pd.read_csv(fall, sep="\t")
df_spring = pd.read_csv(spring, sep="\t")
df_summer = pd.read_csv(summer, sep="\t")


fall_tab, spring_tab, summer_tab = st.tabs(["Fall", "Spring", "Summer"])
with fall_tab:
    st.header("Fall Schedule")
    st.dataframe(df_fall)
with spring_tab:
    st.header("Fall Schedule")
    st.dataframe(df_spring)
with summer_tab:
    st.header("Summer Schedule")
    st.dataframe(df_summer)


