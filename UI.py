import os
import streamlit as st


def render_ui():
  """Safe fallback UI renderer for Aarogya-AI."""
  st.subheader("Aarogya-AI")
  st.write("Personal health and wellness monitoring interface.")


def show_ui():
  render_ui()


def main():
  render_ui()


def get_api_key():
  """Reads GOOGLE_API_KEY from Streamlit Secrets or environment."""
  try:
    if "GOOGLE_API_KEY" in st.secrets:
      return st.secrets["GOOGLE_API_KEY"]
  except Exception:
    pass
  return os.getenv("GOOGLE_API_KEY", "")
