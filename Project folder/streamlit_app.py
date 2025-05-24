
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Display logo at the top left
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="logo.png" width="100" style="margin-right: 10px;">
        <h1 style="margin: 0;">IGT Analysis Tool</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Add custom background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Embed the IGT HTML experiment
with open("igt_with_copy.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=700, scrolling=True)

# Monitor and analyze output data
data_file = "igt_data.txt"
if os.path.exists(data_file):
    df = pd.read_csv(data_file, sep="\t", header=None)

    # Focus on the second column for net scores
    net_scores = df.iloc[:, 1]

    # Calculate z-scores for net scores
    z_scores = (net_scores - net_scores.mean()) / net_scores.std()

    # Calculate total net score
    total_net = net_scores.sum()

    # Categorize participant
    category = "Advantageous" if total_net > 0 else "Disadvantageous"

    # Display summary statistics
    st.write("### Participant Summary")
    st.write(f"Total Net Score: {total_net}")
    st.write(f"Category: {category}")

    # Display data table
    summary_df = pd.DataFrame({
        "Net Score": net_scores,
        "Z-Score": z_scores
    })
    st.dataframe(summary_df)

    # Line plot of net scores
    st.write("### Net Scores Over Trials")
    fig, ax = plt.subplots()
    ax.plot(net_scores, marker='o')
    ax.set_xlabel("Trial")
    ax.set_ylabel("Net Score")
    st.pyplot(fig)

    # Histogram of z-scores
    st.write("### Histogram of Z-Scores")
    fig, ax = plt.subplots()
    ax.hist(z_scores, bins=20, edgecolor='black')
    ax.set_xlabel("Z-Score")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
else:
    st.warning("No data file found yet.")
