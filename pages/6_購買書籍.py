import streamlit as st
import pandas as pd
import os, shutil


def arrive(name, number):
    pass


def main():
    if 'selection' not in st.session_state:
        st.session_state.selection = ""

    paths = os.getcwd()
    paths += "/data/storage"

    st.title("購買書籍清單")

    dataframe = pd.DataFrame([1, 3])
    if dataframe.shape[0] > 0:
        st.write("購買書籍清單\n")
        st.dataframe(dataframe)
    else:
        st.write("無購買書籍")

    dir = ["請選擇書籍"] + ["1", "2", "3", "4"]
    name = st.selectbox("請選擇到貨書籍...", options=dir)
    if name != "請選擇書籍":
        number = st.selectbox("請選擇到貨數量...", options=[0, 1, 2, 3, 4])

        if number > 0:
            st.write(f'''{name} 已到貨{number}本''')
            st.button(
                label="確認到貨",
                on_click=arrive,
                args=[name, number]
            )


if __name__ == "__main__":
    main()
