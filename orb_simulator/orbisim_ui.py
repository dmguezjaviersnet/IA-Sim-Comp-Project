import streamlit as st
from streamlit_ace import st_ace

class OrbisimUI:

    def __init__(self):
        self.code_text = st_ace(keybinding="vscode", theme="monokai", height=500)

    def print_ast(self, text: str):
        st.write(text)
# # code = st_ace()
# st.title("")
# first, second = st.columns(2)
# # with first:
# code = st_ace(keybinding="vscode", theme="monokai", height=500)
# # with second:
# #     st.write(code)