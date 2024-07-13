import streamlit as st
import pandas as pd
import os


def click(file_path):
    df = pd.DataFrame(columns=["書櫃", "手工盤點數量"])
    df.to_csv(file_path, index=False)
    st.session_state.clicked = False


def click_edit_button():
    st.session_state.click_edit_button_state = True


def click_upload_button():
    st.session_state.click_upload_button_state = True


def upload(dataframe, file_path):
    try:
        dataframe = dataframe[["書櫃", "手工盤點數量"]].copy()
        dataframe["書櫃"] = dataframe["書櫃"].astype(str)
        dataframe.to_csv(file_path, index=False)
    except:
        st.session_state.error = True
        st.session_state.message = "上傳格式有誤"
    st.session_state.click_upload_button_state = False
    st.session_state.clicked = False


def click_button(edit_df, file_path):
    edit_df["書櫃"] = edit_df["書櫃"].astype(str)
    edit_df.to_csv(file_path, index=False)
    st.session_state.clicked = False
    st.session_state.click_edit_button_state = False
    st.session_state.confirm = False


def click_confirm():
    st.session_state.confirm = True


def unclick_button():
    st.session_state.clicked = True


def main():
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    if 'click_edit_button_state' not in st.session_state:
        st.session_state.click_edit_button_state = False

    if 'click_upload_button_state' not in st.session_state:
        st.session_state.click_upload_button_state = False
    if 'confirm' not in st.session_state:
        st.session_state.confirm = False

    if 'error' not in st.session_state:
        st.session_state.error = False

    st.title("手工盤點結果新增")
    path = os.getcwd()
    path += "/data"
    dir_list = os.listdir(path)
    dir_list.remove("default")

    name = st.selectbox("請選擇講堂...", dir_list)

    if name:

        path2 = f"{path}/{name}/count"
        dir_list = os.listdir(path2)
        dir_list = [x.replace(".csv", "") for x in dir_list]
    else:
        dir_list = []
    type = st.selectbox("請選擇分區...", dir_list)

    if not type:
        return
    file_path = f"{path}/{name}/count/{type}.csv"
    df = pd.read_csv(file_path)

    if st.session_state.clicked:

        if st.session_state.click_edit_button_state:
            edit_df = st.data_editor(df, num_rows="dynamic")
            if not st.session_state.confirm:
                st.button("確認", on_click=click_confirm)
            else:
                st.button("儲存", on_click=click_button, args=[edit_df, file_path])

        if st.session_state.click_upload_button_state:
            uploaded_file = st.file_uploader("Choose a CSV file")
            if uploaded_file is not None:
                dataframe = pd.read_csv(uploaded_file, index_col=False)
                st.dataframe(dataframe)
                st.button("click to save", on_click=upload, args=[dataframe, file_path])

        if not st.session_state.click_upload_button_state and not st.session_state.click_edit_button_state:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("編輯盤點表", on_click=click_edit_button)
            with col2:
                st.button("上傳盤點表", on_click=click_upload_button)
            with col3:
                st.button("刪除盤點表", on_click=click, args=[file_path])
            st.dataframe(df)

    else:
        st.button("盤點表異動", on_click=unclick_button)
        st.dataframe(df)
        df["書櫃"] = df["書櫃"].astype(str)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="下載盤點表",
            data=csv,
            file_name="盤點表.csv",
            mime="text/csv")

    if st.session_state.error:
        st.error(st.session_state.message)


if __name__ == "__main__":
    main()
