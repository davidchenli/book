import streamlit as st
import pandas as pd
import os, shutil


# def arrive(name):
#
#     pass


def main():
    if 'selection' not in st.session_state:
        st.session_state.selection = ""

    paths = os.getcwd()
    paths += "/data/default/storage"

    st.title("購買書籍清單")

    df_purchase = pd.read_csv(f"{paths}/purchase.csv")
    df_purchase["ISBN"] = df_purchase["ISBN"].astype(str)
    df_purchase["總數"] = 1
    df_purchase = df_purchase.groupby("ISBN")["總數"].count().reset_index()

    df = pd.read_csv(f"{paths}/df2.csv").drop(columns=["Unnamed: 0"])
    dataframe = df_purchase.merge(df, on=["ISBN"])

    if dataframe.shape[0] > 0:
        st.write("購買書籍清單\n")
        st.dataframe(dataframe)
    else:
        st.write("無購買書籍")



if __name__ == "__main__":
    main()
