import streamlit as st

import numpy as np
import pandas as pd

import os, shutil

import csv


def check(code):
    flag1 = code[:3] == "FGS"
    flag2 = len(code) >= 10 and len(code) <= 11
    try:
        int(code[3:])
        flag4 = True
    except:
        flag4 = False

    if flag1 and flag2 and flag4:
        return True
    return False


def click_button(edit_df, file_path):
    edit_df.to_csv(file_path, index=False)
    flag1 = edit_df["條碼號"].notnull()
    flag2 = edit_df["條碼號"] != ""
    edit_df.loc[(flag1 & flag2), "條碼號"].to_csv(file_path, index=False)
    st.session_state.clicked = False


def unclick_button():
    st.session_state.clicked = True


def click_to_delete(name):
    st.session_state.delete_name = name
    st.session_state.click_to_delete = True


def unclick_to_delete():
    st.session_state.click_to_delete = False


def delete(name):
    paths = os.getcwd()
    paths += "/data"
    shutil.rmtree(f"{paths}/{name}")
    st.session_state.click_to_delete = False
    st.session_state.click_to_delete = False


def main():
    paths = os.getcwd()
    paths += "/data"
    if 'click_to_delete' not in st.session_state:
        st.session_state.click_to_delete = False

    if 'delete_name' not in st.session_state:
        st.session_state.delete_name = ""

    st.title("報表產出")
    if st.session_state.click_to_delete:
        st.button("上一頁", on_click=unclick_to_delete)
        st.write(st.session_state.delete_name)
        st.button("一鍵清除資料", on_click=delete, args=[st.session_state.delete_name])
        return

    dir_list = os.listdir(paths)
    dir_list = [x for x in dir_list if "csv" not in x]
    name = st.selectbox("請選擇講堂...", dir_list)
    if name is None:
        return

    path2 = f"{paths}/{name}/count"
    dir_list = os.listdir(path2)
    dir_list = [x.replace(".csv", "") for x in dir_list]

    issue = pd.DataFrame(columns=["分區", "書櫃"])
    output = {}
    out_df = pd.DataFrame()
    output_df = pd.DataFrame()
    expect_number = 0
    for x in dir_list:
        path2 = f"{paths}/{name}/count/{x}.csv"
        df = pd.read_csv(path2)
        df["書櫃"] = df["書櫃"].astype(str)
        expect_number += sum(df["手工盤點數量"])
        path = f"{paths}/{name}/real/{x}"
        dir = os.listdir(path)
        df3 = pd.DataFrame(columns=["書櫃", "duplicates", "number_fail", "number_success"])
        for d in dir:
            df2 = pd.read_csv(f"{paths}/{name}/real/{x}/" + d)
            df2["check"] = df2["條碼號"].apply(check)
            success = set(df2.loc[df2["check"], "條碼號"].to_list())

            duplicates = sum(df2["check"]) - len(success)
            fail = sum(~df2["check"])
            temp = pd.DataFrame([[d.replace(".csv", ""), duplicates, fail, len(success)]],
                                columns=["書櫃", "重複的條碼數", "錯誤條碼數", "正確條碼數"])

            out = pd.DataFrame(success, columns=["條碼號"])
            out["書櫃"] = d
            out_df = pd.concat([out_df, out])
            df3 = pd.concat([df3, temp])

        out = df.merge(df3, how="left", on="書櫃").fillna(0)
        out["分區"] = x
        output[x] = out[["書櫃", "手工盤點數量", "重複的條碼數", "錯誤條碼數", "正確條碼數"]]
        issue_flag = (out["重複的條碼數"] != 0) | (out["錯誤條碼數"] != 0) | (
                out["正確條碼數"] != out["手工盤點數量"])
        df_out = out[issue_flag]
        issue = pd.concat([issue, df_out[["分區", "書櫃"]]])
        output_df = pd.concat([output_df, out])

    st.dataframe(issue)
    st.write(f'''{name} 一共盤點 {len(out_df["條碼號"])} 本書,預期應有 {expect_number} 本''')
    col1, col2, col3 = st.columns(3)
    with col1:

        st.download_button(
            label="一鍵匯出報表",
            data=output_df.to_csv(index=False).encode("utf-8"),
            file_name="large_df.csv",
            mime="text/csv")

    with col2:

        st.download_button(
            label="一鍵匯出條碼號",
            data=out_df.to_csv(index=False).encode("utf-8"),
            file_name="large_df.txt")
        # mime="text/csv")

    with col3:
        st.button("清除資料", on_click=click_to_delete, args=[name])

    if len(dir_list):
        outs = st.tabs(dir_list)
        for x, y in zip(dir_list, outs):
            with y:
                st.header(x)
                st.dataframe(output[x])


if __name__ == "__main__":
    main()
