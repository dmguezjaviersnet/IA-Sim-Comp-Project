import streamlit as st
from streamlit_ace import st_ace
from compile_and_execute import orbsim_compile_and_execute
from io import StringIO  
import sys
class OrbisimUI:
    
    def __init__(self, handler):
        # self.code_text = st_ace(keybinding="vscode", theme="monokai", height=500)
        
        # st.write('Console Output:')
        # exe_cu =orbsim_compile_and_execute(code)
        # st.write(exe_cu)
        self.editor(handler)

    
    def editor(self, handler):
        self.title = st.title("OrbiSimulatorCode")
        self.handler = handler
        
        # editor = st.text_area('')
        # button = st.button('Compile ans Run')
        # if button:
        #     text = editor.title()
        #     orbsim_compile_and_execute(text)
        first, second = st.columns([10, 2])
        with first:
           
            code = st_ace(wrap= True)
            if code :
                capture_io_file = StringIO()
                sys.stdout = capture_io_file
                errs = orbsim_compile_and_execute(code, handler)
                if errs:
                    st.error('❌Errors found❌')
                    for err in errs:
                        st.write(err)
                else:
                    all_output =str(capture_io_file.getvalue()).split('\n')
                    st.success('✅The orbsim code compile and execute succeded') 
                    for i in all_output:
                        if i:
                            st.write(i)

    
# # code = st_ace()
# st.title("")
# first, second = st.columns(2)
# # with first:
# code = st_ace(keybinding="vscode", theme="monokai", height=500)
# # with second:
# #     st.write(code)