import streamlit as st
import psutil
import pandas as pd
import plotly.express as px

# Logo
st.image("images/image.png", width=250)

# Header and description
text_col, button_col = st.columns([2.8, 1])
with text_col:
    st.subheader("WSL RESOURCE DASHBOARD")
    st.text("Monitor the WSL system resources")

# Metric columns
cpu_col, tmem_col, amem_col, swap_col = st.columns(4)


# Function to get and display system info
def system_info():
    cpu_percent = psutil.cpu_percent()
    memory_total = psutil.virtual_memory().total / (1024**3)  # GB
    memory_available = psutil.virtual_memory().available / (1024**3)
    swap_memory = psutil.swap_memory().total / (1024**3)

    with cpu_col:
        st.metric("CPU Usage", f"{cpu_percent:.1f}%")
    with tmem_col:
        st.metric("Total Memory", f"{memory_total:.1f} GB")
    with amem_col:
        st.metric("Available Memory", f"{memory_available:.1f} GB")
    with swap_col:
        st.metric("Swap Memory", f"{swap_memory:.1f} GB")

    # Return memory data for bar chart in GB
    return pd.DataFrame(
        {
            "resources": ["Total Memory", "Available Memory", "Swap Memory"],
            "usage": [memory_total, memory_available, swap_memory],
        }
    ).set_index("resources")


# Button to update metrics
data = None
with button_col:
    if st.button("Refresh"):
        data = system_info()

# Display bar chart below metrics if data exists
if data is not None:
    fig = px.bar(
        data,
        x=data.index,
        y="usage",
        text=data["usage"].map(lambda x: f"{x:.1f} GB"),
        labels={"usage": "GB", "resources": "Resources"},
        width=500,
        height=500,
    )
    fig.update_traces(textposition="outside", marker_color="orange")
    st.plotly_chart(fig)
