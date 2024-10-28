import streamlit as st

import pandas as pd
import os
import csv


def purchase():
    st.session_state.text_key = ''


def cancel():
    st.session_state.text_key = ''


def main():
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
    if 'error' not in st.session_state:
        st.session_state.error = False

    st.title("館藏比對")
    path = os.getcwd()
    path += "/data"

    st.text_input(
        "請輸入ISBN號",
        key='text_key'
    )

    if st.session_state.text_key != "":

        st.title("查詢結果")

        name = "name"
        if name:
            st.write(f'''書名: {name}''')
        else:
            st.write("查無書名")

        number = 1
        st.write(f'''館藏數量:{number}''')

        number2 = 12
        st.write(f'''已購買數量:{number2}''')

        dataframe = pd.DataFrame([1, 3])
        if dataframe.shape[0] > 0:
            st.write("出版商資料\n")
            st.dataframe(dataframe)
        else:
            st.write("查無出版商資料")

        col1, col2 = st.columns(2)
        with col1:

            st.button(
                label="確認購買",
                on_click=purchase
            )

        with col2:

            st.button(
                label="取消",
                on_click=cancel
            )


if __name__ == "__main__":
    main()
