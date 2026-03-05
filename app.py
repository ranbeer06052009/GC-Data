import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Frammer AI Analytics Dashboard")

# -------------------------
# Load datasets
# -------------------------

@st.cache_data
def load_data():
    monthly = pd.read_csv("data/monthly-chart.csv")
    duration = pd.read_csv("data/month-wise-duration.csv")
    videos = pd.read_csv("data/video_list_data_obfuscated.csv")

    channel = pd.read_csv("data/CLIENT 1 combined_data(2025-3-1-2026-2-28).csv")
    user = pd.read_csv("data/combined_data(2025-3-1-2026-2-28) by user.csv")
    language = pd.read_csv("data/combined_data(2025-3-1-2026-2-28) by language.csv")
    input_type = pd.read_csv("data/combined_data(2025-3-1-2026-2-28) by input type.csv")
    output_type = pd.read_csv("data/combined_data(2025-3-1-2026-2-28) by output type.csv")

    return monthly, duration, videos, channel, user, language, input_type, output_type

monthly, duration, videos, channel, user, language, input_type, output_type = load_data()

# -------------------------
# Sidebar Navigation
# -------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Summary",
        "Usage Trends",
        "Channel Analysis",
        "User Analysis",
        "Content Analysis",
        "Video Explorer",
    ],
)

# -------------------------
# Executive Summary
# -------------------------

if page == "Executive Summary":

    uploaded = monthly["Total Uploaded"].sum()
    created = monthly["Created"].sum()
    published = monthly["Published"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Uploaded Videos", uploaded)
    col2.metric("Processed Videos", created)
    col3.metric("Published Videos", published)

    publish_rate = round(published / created * 100, 2)

    st.metric("Publish Conversion Rate", f"{publish_rate}%")

    st.subheader("Processing Funnel")

    funnel_df = pd.DataFrame(
        {
            "Stage": ["Uploaded", "Created", "Published"],
            "Count": [uploaded, created, published],
        }
    )

    fig = px.funnel(funnel_df, x="Count", y="Stage")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Usage Trends
# -------------------------

elif page == "Usage Trends":

    st.subheader("Monthly Usage")

    fig = px.line(
        monthly,
        x="Month",
        y=["Uploaded", "Created", "Published"],
        markers=True,
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Duration")

    fig2 = px.bar(
        duration,
        x="Month",
        y=["Uploaded Duration", "Created Duration", "Published Duration"],
    )

    st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Channel Analysis
# -------------------------

elif page == "Channel Analysis":

    st.subheader("Channel Performance")

    channel["Publish Rate"] = channel["Published"] / channel["Created"]

    fig = px.bar(
        channel.sort_values("Created", ascending=False),
        x="Channel",
        y="Created",
        title="Videos Processed by Channel",
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        channel,
        x="Channel",
        y="Publish Rate",
        title="Publish Rate by Channel",
    )

    st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# User Analysis
# -------------------------

elif page == "User Analysis":

    st.subheader("Top Users")

    user["Publish Rate"] = user["Published"] / user["Created"]

    fig = px.bar(
        user.sort_values("Created", ascending=False).head(15),
        x="Uploaded By",
        y="Created",
        title="Top Users by Processing",
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        user,
        x="Uploaded By",
        y="Publish Rate",
        title="User Publish Efficiency",
    )

    st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Content Analysis
# -------------------------

elif page == "Content Analysis":

    st.subheader("Language Distribution")

    fig = px.pie(
        language,
        names="Language",
        values="Created",
    )

    st.plotly_chart(fig)

    st.subheader("Input Type")

    fig2 = px.bar(
        input_type,
        x="Input Type",
        y="Created",
    )

    st.plotly_chart(fig2)

    st.subheader("Output Type")

    fig3 = px.bar(
        output_type,
        x="Output Type",
        y="Created",
    )

    st.plotly_chart(fig3)

# -------------------------
# Video Explorer
# -------------------------

elif page == "Video Explorer":

    st.subheader("Video Database")

    search = st.text_input("Search headline")

    if search:
        filtered = videos[videos["Headline"].str.contains(search, case=False)]
    else:
        filtered = videos

    st.dataframe(filtered)