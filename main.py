import streamlit as st
import pandas as pd
import plotly.express as px



df = pd.read_csv("Data.csv")


df["CONSUMPTION"] = pd.to_numeric(
    df["CONSUMPTION"],
    errors="coerce"
)


df = df.dropna(
    subset=["COUNTRY", "PRODUCT", "CONSUMPTION", "YEAR"]
)


df = df[df["CONSUMPTION"] >= 0]



st.title("☀️ Solar Energy Consumption")




country = st.selectbox(
    "Select Country",
    sorted(df["COUNTRY"].unique())
)




country_data = df[df["COUNTRY"] == country]


product_data = country_data.groupby(
    ["COUNTRY", "PRODUCT"],
    as_index=False
)["CONSUMPTION"].sum()

product_data = product_data[
    product_data["CONSUMPTION"] > 0
]




col1, col2 = st.columns(2)


with col1:

    fig = px.sunburst(
        product_data,
        path=["COUNTRY", "PRODUCT"],
        values="CONSUMPTION"
    )

    fig.update_layout(
        height=600,
        margin=dict(
            t=30,
            l=10,
            r=10,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )



with col2:

    total_consumption = country_data["CONSUMPTION"].sum()

    table_data = pd.DataFrame({
        "COUNTRY": [country],
        "CONSUMPTION": [total_consumption]
    })

    st.dataframe(
        table_data,
        width="stretch",
        hide_index=True,
        height=100
    )




year_data = df.groupby(
    "YEAR",
    as_index=False
)["CONSUMPTION"].sum()


fig2 = px.bar(
    year_data,
    x="YEAR",
    y="CONSUMPTION",color="CONSUMPTION",
    color_continuous_scale="Viridis",
    
    title="Overall Year-wise Solar Energy Consumption",
    text="CONSUMPTION"
)


fig2.update_traces(
    texttemplate="%{y:.0f}",
    textposition="outside"
)


st.plotly_chart(
    fig2,
    width="stretch"
)