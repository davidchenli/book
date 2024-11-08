import streamlit as st

import pandas as pd
import os
import csv


def purchase():
    path = os.getcwd()
    path += "/data/default/storage"
    file_path = f'''{path}/purchase.csv'''
    with open(file_path, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([st.session_state.text_key])
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
    path += "/data/default/storage"

    st.text_input(
        "請輸入ISBN號",
        key='text_key'
    )

    if st.session_state.text_key != "":

        df = pd.read_csv(f"{path}/df2.csv").drop(columns=["Unnamed: 0"])
        df["ISBN"] = df["ISBN"].astype(str)
        df_storage = pd.read_csv(f"{path}/df_out.csv").drop(columns=["Unnamed: 0"])
        df_storage["ISBN"] = df_storage["ISBN"].astype(str)
        df_p = pd.read_csv(f"{path}/df3.csv").drop(columns=["Unnamed: 0"])
        df_p["ISBN"] = df_p["ISBN"].astype(str)

        dataframe = df[df["ISBN"] == st.session_state.text_key]

        dataframe2 = df_storage[df_storage["ISBN"] == st.session_state.text_key]
        dataframe4 = df_p[df_p["ISBN"] == st.session_state.text_key]
        st.title("查詢結果")

        if dataframe.shape[0] > 0:
            name = dataframe["書名"].values[0]
            st.write(name)
            st.write("出版商資料\n")
            st.dataframe(dataframe)
        else:
            st.write("查無出版商資料")

        if dataframe2.shape[0] > 0:

            number = dataframe2["條碼號"].values[0]
            st.write(f'''館藏數量:{number}''')
        else:
            st.write("查無館藏資料")

        df_purchase = pd.read_csv(f"{path}/purchase.csv")
        df_purchase["ISBN"] = df_purchase["ISBN"].astype(str)
        dataframe3 = df_purchase[df_purchase["ISBN"] == st.session_state.text_key]

        st.write(f'''已購買數量:{dataframe3.shape[0]}''')
        st.write(f'''基金會購買數量:{dataframe4.shape[0]}''')

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
