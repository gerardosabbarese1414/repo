import streamlit as st
import pandas as pd

st.title("Boot to lead !")
st.subheader("Ciao Ciccio")
st.camera_input('label')

data_df = pd.DataFrame(
    {
        "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
        "favorite": [True, False, False, True],
        "colore": ["verde", "rosso", "blu"]
    }
)

st.data_editor(
    data_df,
    column_config={
        "favorite": st.column_config.CheckboxColumn(
            "Your favorite?",
            help="Select your **favorite** widgets",
            default=False,


        )
    },
    disabled=["widgets"],

    hide_index=True,
)
