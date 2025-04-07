# app.py

import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Email Assistant", layout="wide")

st.title("📬 Email Assistant Dashboard")

if st.button("Run Assistant"):
    st.success("Running backend...")
    result = subprocess.run(
        ["python", "-m", "src.controllers.main"],
        capture_output=True,
        text=True
    )
    st.code(result.stdout)  # Shows the output of terminal process
    st.error(result.stderr) if result.stderr else None
