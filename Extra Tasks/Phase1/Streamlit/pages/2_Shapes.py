import streamlit as st
import time

st.header("Shapes Calculation")
st.sidebar.title("Configrations")

with st.sidebar:
    shape = st.selectbox("Select the Shape", ["Circle", "Rectangle"])

if shape == "Circle":
    radius=st.number_input("Enter the radius of the circle", min_value=0.0,
                     max_value=1000.0, step = 1.0)
    area=3.14*radius*radius
    perimeter=2*3.14*radius

else:
    length=st.number_input("Length", min_value=0.0, max_value=1000.0, step = 1.0)
    Width=st.number_input("Width", min_value=0.0, max_value=1000.0, step = 1.0)
    area=length*Width
    perimeter=2*(length+Width)

compute_button=st.button("Compute Area and Perimeter")

if compute_button:
    with st.spinner("Calculating..."):
        time.sleep(1)
        st.write(f"Area of the {shape} is: ", area)
        st.write(f"Perimeter of the {shape} is: ", perimeter)
