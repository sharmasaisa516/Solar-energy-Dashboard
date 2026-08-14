import pandas as pd
import plotly.express as px
import requests
import streamlit as st


st.set_page_config(
    page_title="Solar Energy Dashboard", page_icon="☀️", layout="wide"
)


OLLAMA_MODEL = "gemma3:270m"
OLLAMA_URL = "http://localhost:11434/api/chat"


SYSTEM_PROMPT = """
You are 'Solar AI', an intelligent, concise, and friendly assistant embedded in a Solar Energy Dashboard.
Your role is to help users analyze solar energy data, understand dashboard charts, and answer questions about solar power.

Dashboard Context:
1. Home Page: Global Choropleth map of solar consumption, country details, metrics (total, monthly avg, peak month), and line trend charts.
2. Uses of Solar Energy Page: 10 main applications of solar power (electricity, water heating, cooking, street lighting, agriculture, etc.) and global year-wise bar charts.
3. Analysis of Solar Energy Page: KPI metric cards (Top Installed, Highest Consumption country, Carbon Offset), product-wise Sunburst charts, and consumption breakdown tables.

Guidelines:
- Give short, crisp, and helpful answers.
- Use emojis where appropriate.
- Answer user queries related to solar energy, data analysis, and green technology.
"""


def query_ollama(messages):
    """Sends chat messages to local Ollama instance."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
            },
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            return f"❌ Ollama Error ({response.status_code}). Please check if the model `{OLLAMA_MODEL}` is pulled."
    except Exception as e:
        return f"⚠️ Connection error. Please ensure Ollama is running (`ollama run {OLLAMA_MODEL}`)."



if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "assistant",
            "content": "Hello! ☀️ Main aapka Solar AI Assistant hoon. Dashboard ya solar energy se juda koi bhi sawal puchiye!",
        },
    ]



top_col1, top_col2 = st.columns([0.85, 0.15])
with top_col2:
    with st.popover("💬 Chat AI", use_container_width=True):
        st.subheader("🤖 Solar AI Assistant (`gemma3:270m`)")
        st.caption("Powered by local Ollama model")

        
        for msg in st.session_state.chat_messages:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        
        if prompt := st.chat_input("Puchiye solar energy ke baare me..."):
            
            st.session_state.chat_messages.append(
                {"role": "user", "content": prompt}
            )
            with st.chat_message("user"):
                st.write(prompt)

            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response_text = query_ollama(st.session_state.chat_messages)
                    st.write(response_text)

            
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": response_text}
            )



@st.cache_data
def load_data():
    df = pd.read_csv("Data.csv")
    return df



st.sidebar.title("Solar Energy Dashboard")
page = st.sidebar.radio(
    "Go to:", ["Home", "Uses of Solar Energy", "Analysis of Solar Energy"]
)



if page == "Analysis of Solar Energy":
    st.title("☀️ Analysis of Solar Energy Uses")
    st.write(
        "Solar energy is used to generate electricity, heat water, and power "
        "homes and industries. It is a clean, renewable, and eco-friendly source of energy."
    )

    st.subheader("📊 Solar Energy Highlights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div style="background-color:#fff3cd; padding:20px; border-radius:15px; text-align:center; height:250px; box-shadow:2px 2px 10px #cccccc;">
            <h3 style="color:#222222;">☀️ Top Solar Installed</h3>
            <h2 style="color:#222222;">2026</h2>
            <p style="color:#222222;">Total solar capacity installed</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div style="background-color:#d4edda; padding:20px; border-radius:15px; text-align:center; height:250px; box-shadow:2px 2px 10px #cccccc;">
            <h3 style="color:#222222;">📍 Top Solar Country</h3>
            <h2 style="color:#222222; font-size:22px;">United States highest solar consumption (~8,25,910)</h2>
            <p style="color:#222222;"></p>     
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div style="background-color:#d1ecf1; padding:20px; border-radius:15px; text-align:center; height:250px; box-shadow:2px 2px 10px #cccccc;">
            <h3 style="color:#222222;">🌱 Carbon Offset</h3>
            <h2 style="color:#222222;">2026</h2>
            <p style="color:#222222;">CO₂ emissions reduced through solar energy</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.divider()

    df = load_data()
    df["CONSUMPTION"] = pd.to_numeric(df["CONSUMPTION"], errors="coerce")
    df = df.dropna(subset=["COUNTRY", "PRODUCT", "CONSUMPTION", "YEAR"])
    df = df[df["CONSUMPTION"] >= 0]

    st.title("☀️ Solar Energy Consumption")

    country = st.selectbox("Select Country", sorted(df["COUNTRY"].unique()))
    country_data = df[df["COUNTRY"] == country]

    product_data = country_data.groupby(
        ["COUNTRY", "PRODUCT"], as_index=False
    )["CONSUMPTION"].sum()
    product_data = product_data[product_data["CONSUMPTION"] > 0]

    st.markdown("### 📊 Energy Consumption Breakdown")

    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        st.markdown("#### ☀️ Sunburst Chart")
        fig = px.sunburst(
            product_data,
            path=["COUNTRY", "PRODUCT"],
            values="CONSUMPTION",
            color="CONSUMPTION",
            color_continuous_scale="Viridis",
        )
        fig.update_layout(height=450, margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📋 Consumption Summary")
        total_consumption = country_data["CONSUMPTION"].sum()

        st.metric(
            label=f"Total Solar Consumption ({country})",
            value=f"{total_consumption:,.2f}",
        )
        st.markdown("---")
        st.caption("Product-wise Breakdown:")
        st.dataframe(
            product_data[["PRODUCT", "CONSUMPTION"]].sort_values(
                by="CONSUMPTION", ascending=False
            ),
            use_container_width=True,
            hide_index=True,
            height=220,
        )



elif page == "Uses of Solar Energy":
    st.title("🔋 Uses of Solar Energy")
    st.write(
        "Solar energy is used to generate electricity through solar panels "
        "and to heat water and buildings. It is a clean and renewable source "
        "of energy that helps reduce pollution and electricity costs."
    )

    st.divider()

    col1, col2 = st.columns([1, 1], vertical_alignment="center")

    with col1:
        st.markdown("""
        ☀️ **1. Electricity Generation**  
        Solar panels convert sunlight into electricity for homes and businesses.

        ☀️ **2. Water Heating**  
        Solar water heaters use sunlight to heat water.

        ☀️ **3. Cooking**  
        Solar cookers use sunlight to cook food without using gas or electricity.

        ☀️ **4. Agriculture**  
        Solar energy is used to operate water pumps for irrigation.

        ☀️ **5. Street Lighting**  
        Solar street lights store energy during the day and provide light at night.

        ☀️ **6. Heating Buildings**  
        Solar energy can be used to heat homes and buildings.

        ☀️ **7. Charging Devices**  
        Solar chargers can charge mobile phones, batteries, and other devices.

        ☀️ **8. Transportation**  
        Solar energy can provide electricity for electric vehicles and charging stations.

        ☀️ **9. Industrial Use**  
        Industries use solar energy for electricity, heating, and different production processes.

        ☀️ **10. Rural Electrification**  
        Solar power can provide electricity to remote areas where electricity connections are difficult.
        """)

    with col2:
        st.image(
            "1.png", caption="Solar Panels in Action", use_container_width=True
        )

    st.divider()

    df = load_data()
    df["CONSUMPTION"] = pd.to_numeric(df["CONSUMPTION"], errors="coerce")
    df = df.dropna(subset=["COUNTRY", "PRODUCT", "CONSUMPTION", "YEAR"])
    df = df[df["CONSUMPTION"] >= 0]

    year_data = df.groupby("YEAR", as_index=False)["CONSUMPTION"].sum()

    fig2 = px.bar(
        year_data,
        x="YEAR",
        y="CONSUMPTION",
        color="CONSUMPTION",
        color_continuous_scale="Viridis",
        title="Overall Year-wise Solar Energy Consumption",
        text="CONSUMPTION",
    )
    fig2.update_traces(texttemplate="%{y:.0f}", textposition="outside")
    fig2.update_layout(height=500, margin=dict(t=50, l=10, r=10, b=10))

    st.plotly_chart(fig2, use_container_width=True)



elif page == "Home":
    st.title("📊 Solar Energy Consumption")
    st.write(
        "Solar energy consumption has been increasing globally as more "
        "people recognize its benefits. This dashboard provides an analysis "
        "of solar energy consumption across different countries, products, "
        "and years. Select a country on the map or from the dropdown to see "
        "detailed consumption data."
    )
    st.divider()

    df = load_data()
    solar_df = df[df["PRODUCT"] == "Solar"]

    country_totals = (
        solar_df.groupby("COUNTRY", as_index=False)["CONSUMPTION"]
        .sum()
        .rename(columns={"CONSUMPTION": "TOTAL_CONSUMPTION"})
    )

    st.subheader("🗺️ World Map - Total Solar Consumption")

    fig_map = px.choropleth(
        country_totals,
        locations="COUNTRY",
        locationmode="country names",
        color="TOTAL_CONSUMPTION",
        color_continuous_scale="Viridis",
        hover_name="COUNTRY",
        labels={"TOTAL_CONSUMPTION": "Solar Consumption"},
        range_color=[0, 1000000],
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=10, b=0))

    st.plotly_chart(fig_map, use_container_width=True)

    st.divider()

    st.subheader("🔎 Select a Country for Details")
    countries = sorted(country_totals["COUNTRY"].unique())
    selected_country = st.selectbox("Country choose karein:", countries)

    country_data = solar_df[solar_df["COUNTRY"] == selected_country]

    total = country_data["CONSUMPTION"].sum()
    avg = country_data["CONSUMPTION"].mean()

    
    if not country_data.empty and "MONTH_NAME" in country_data.columns:
        peak_row = country_data.loc[country_data["CONSUMPTION"].idxmax()]
        peak_info = f"{peak_row['MONTH_NAME']} {int(peak_row['YEAR'])}"
    else:
        peak_info = "N/A"

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Consumption", f"{total:,.2f}")
    col2.metric("Average (per month)", f"{avg:,.2f}")
    col3.metric("Peak Month", peak_info)

    yearly = country_data.groupby("YEAR", as_index=False)["CONSUMPTION"].sum()
    fig_trend = px.line(
        yearly,
        x="YEAR",
        y="CONSUMPTION",
        markers=True,
        title=f"{selected_country} - Yearly Solar Consumption Trend",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    with st.expander("📄 Detailed Data"):
        st.dataframe(
            country_data[["YEAR", "MONTH_NAME", "CONSUMPTION"]]
            .sort_values(["YEAR"])
            .reset_index(drop=True)
        )