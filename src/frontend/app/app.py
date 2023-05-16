import plotly.express as px 
import numpy as np
import streamlit as st
from streamlit import session_state
from classes.queries import Queries

def main():
    st.set_page_config(page_title="Ice Cream Empire Dashboard", page_icon=":memo:", layout="wide")
    db = Queries()
   

    pages = [f"Page {i+1}" for i in range(8)]
    if not "page" in session_state:
        session_state.page = pages[0]

    for page in pages:
        if st.sidebar.button(page):
            session_state.page = page

    if not "data" in session_state:
        session_state.data = {page: [] for page in pages}

    st.title(session_state.page)

    with st.form(key="input_form"):
        input1 = st.text_input("Input 1")
        input2 = st.text_input("Input 2")
        input3 = st.text_input("Input 3")
        submit_button = st.form_submit_button(label="Submit")

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig = px.scatter(x=x, y=y)
    st.plotly_chart(fig)

    fig = px.scatter(x=x, y=y)
    st.plotly_chart(fig)
    
    if submit_button:
        session_state.data[session_state.page].append([input1, input2, input3])

    for i, row in enumerate(session_state.data[session_state.page]):
        cols = st.columns(4)
        cols[0].write(row[0])
        cols[1].write(row[1])
        cols[2].write(row[2])
        if cols[3].button("Delete", key=f"delete_{i}"):
            del session_state.data[session_state.page][i]

if __name__ == "__main__":
    main()