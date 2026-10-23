import streamlit as st
import io
import contextlib

st.set_page_config(page_title="Python Code Runner", page_icon="🐍")

st.title("🐍 Python Code Runner")
st.write("Write your Python code, then click Run Code.")

default_code = '''name = "Mohamed"
for i in range(3):
    print(f"Hello {name}! {i + 1}")
'''

code = st.text_area(
    "Your Python code",
    value=default_code,
    height=300,
    key="python_code"
)

if st.button("▶ Run Code", type="primary"):
    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(compile(code, "<user_code>", "exec"), {})

        st.success("Code executed.")
        st.subheader("Output")
        st.code(output.getvalue() or "Code finished without output.")

    except Exception as e:
        st.error(f"{type(e).__name__}: {e}")
        st.subheader("Output before the error")
        st.code(output.getvalue() or "No output.")
