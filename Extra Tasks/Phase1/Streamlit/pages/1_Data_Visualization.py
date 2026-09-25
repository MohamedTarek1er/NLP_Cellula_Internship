import streamlit as st
import pandas as pd
import plotly.express as px

file = st.file_uploader("Upload File", type=["csv", "xlsx"])
if file is not None:
    df=pd.read_csv(file)

    n_rows=st.slider("Select Number of rows", min_value=1, max_value=len(df),step=1, value=5)
    columns_to_show = st.multiselect("Select Columns", df.columns.tolist(), default=df.columns.tolist())

    st.write(df[:n_rows][columns_to_show])

    tab1, tab2 = st.tabs(["Scatter Plot", "Histogram"])

    with tab1:
        col1, col2, col3 = st.columns(3)

        with col1:
            x_column = st.selectbox("Select Column for X Axis", df.columns.tolist())
        with col2:
            y_column = st.selectbox("Select Column for Y Axis", df.columns.tolist())
        with col3:
            color_column = st.selectbox("Select Column for Color", df.columns.tolist())

        fig_scatter=px.scatter(df,x=x_column, y=y_column, color=color_column)
        st.plotly_chart(fig_scatter)

    with tab2:
        hist_column = st.selectbox("Select Column for histogram", df.columns.tolist())
        fig_hist=px.histogram(df, x=hist_column)

        st.plotly_chart(fig_hist)

