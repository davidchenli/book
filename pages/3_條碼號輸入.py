import streamlit as st

import numpy as np
import pandas as pd
import time
# from beepy import beep



import os

import csv

def click_upload_button():
    st.session_state.click_upload_button_state = True
def upload(exe,dataframe, file_path):
    if exe:
        dataframe.to_csv(file_path, index=False)
    st.session_state.click_upload_button_state = False
    st.session_state.clicked = False


def click_edit_button():
    st.session_state.click_edit_button_state = True


def proc(file_path: str, code_list: list):
    code = st.session_state.text_key
    code = code.upper()
    flag1 = code[:3] == "FGS"
    flag2 = len(code) >= 10 and len(code) <= 11
    try:
        int(code[3:])
        flag4 = True
    except:
        flag4 = False

    flag5 = code not in code_list

    if flag1 and flag2 and flag4 and flag5:
        st.session_state.error = False
        with open(file_path, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([code])
    elif not (flag1 and flag2 and flag4):
        st.session_state.error = True
        st.session_state.message = "條碼號不符合預期"
    elif not flag5:
        st.session_state.error = True
        st.session_state.message = "條碼號重複"
    st.session_state.text_key = ''


def click_button(edit_df, file_path):
    update_df = edit_df.astype(str)
    update_df.to_csv(file_path, index=False)
    st.session_state.clicked = False
    st.session_state.click_edit_button_state = False
    st.session_state.confirm = False


def unclick_button():
    st.session_state.clicked = True


def click(file_path):
    df = pd.DataFrame(columns=["條碼號"])
    df.to_csv(file_path, index=False)
    st.session_state.clicked = False


def click_confirm():
    st.session_state.confirm = True


def click_remove(file_path, df):
    df = df[df["條碼號"].notnull()].copy()
    df = df[df["條碼號"] != ""]
    df = df[df["條碼號"] != "nan"]
    df = df["條碼號"].drop_duplicates()
    df.to_csv(file_path, index=False)
    st.session_state.clicked = False


def main():
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
    if 'error' not in st.session_state:
        st.session_state.error = False

    if 'message' not in st.session_state:
        st.session_state.message = ""

    if 'success' not in st.session_state:
        st.session_state.success = False

    if 'click_edit_button_state' not in st.session_state:
        st.session_state.click_edit_button_state = False
    if 'sleep' not in st.session_state:
        st.session_state.sleep = False
    if 'confirm' not in st.session_state:
        st.session_state.confirm = False

    if 'click_upload_button_state' not in st.session_state:
        st.session_state.click_upload_button_state = False

    st.title("條碼號盤點")
    path = os.getcwd()
    path += "/data"

    col1, col2 = st.columns(2)
    with col1:
        dir_list = os.listdir(path)
        dir_list = [x for x in dir_list if "csv" not in x]
        name = st.selectbox("請選擇講堂...", dir_list)
    with col2:
        if name:
            path2 = f"{path}/{name}/count"
            dir_list = os.listdir(path2)
            dir_list = [x.replace(".csv", "") for x in dir_list]
            type = st.selectbox("請選擇分區...", dir_list)
            if not type:
                return
        else:
            return

    file_path = f"{path}/{name}/count/{type}.csv"
    df = pd.read_csv(file_path)
    df = df.astype(str)
    room_list = df["書櫃"].to_list()
    room = st.selectbox("請選擇書櫃...", room_list)

    if not room:
        return

    df["手工盤點數量"] = df["手工盤點數量"].astype(int)
    target = sum(df[df["書櫃"] == room]["手工盤點數量"])
    file_path = f"{path}/{name}/real/{type}/{room}.csv"
    try:
        df = pd.read_csv(file_path)
        df = df.astype(str)
    except:
        df = pd.DataFrame(columns=["條碼號"])
        df.to_csv(file_path, index=False)

    if st.session_state.clicked:
        if st.session_state.click_edit_button_state:
            edit_df = st.data_editor(df, num_rows="dynamic")
            if not st.session_state.confirm:
                st.button("確認", on_click=click_confirm)
            else:
                st.button("儲存當前修改", on_click=click_button, args=[edit_df, file_path])
        elif st.session_state.click_upload_button_state:
            uploaded_file = st.file_uploader("點擊上傳條碼號")
            if uploaded_file is not None:
                dataframe = pd.read_csv(uploaded_file, index_col=False)
                st.dataframe(dataframe)
                st.button("儲存", on_click=upload, args=[True,dataframe, file_path])
                st.button("取消", on_click=upload, args=[False, dataframe, file_path])
        else:

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.button("編輯條碼號", on_click=click_edit_button)
                st.dataframe(df)
            with col2:
                st.button("上傳條碼號", on_click=click_upload_button)
            with col3:
                st.button("去除重複無效條碼號", on_click=click_remove, args=[file_path, df])

            with col4:
                st.button("刪除條碼號", on_click=click, args=[file_path])


    else:
        st.button("條碼號異動", on_click=unclick_button)
        st.dataframe(df)
        st.text_input(
            "請輸入條碼號",
            key='text_key',
            on_change=proc,
            args=[file_path, df["條碼號"].to_list()]
        )
    if st.session_state.error:
        # beep(sound='error')
        st.error(st.session_state.message)

    st.write(f"已處理條碼號/條碼號總數 {df['條碼號'].nunique()}/{target}")


if __name__ == "__main__":
    main()
