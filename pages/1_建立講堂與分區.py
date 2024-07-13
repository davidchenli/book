import streamlit as st
import pandas as pd
import os


def submit_comfirm():
    st.session_state.submit_form = True


def submit(exe, name_value, type_value, dir_list, type_list):
    path = os.getcwd()
    path += "/data"

    st.session_state.text_key2 = ""
    st.session_state.error = False
    st.session_state.success = False
    st.session_state.submit_form = False
    if exe:
        if name_value in dir_list:
            if type_value in type_list:
                st.session_state.error = True
            else:
                df = pd.DataFrame(columns=["書櫃", "手工盤點數量"])
                df.to_csv(f"{path}/{name_value}/count/{type_value}.csv", index=False)
                os.mkdir(f"{path}/{name_value}/real/{type_value}")
                df = pd.DataFrame(columns=["default"])
                df.to_csv(f"{path}/{name_value}/real/{type_value}.csv", index=False)
                st.session_state.success = True
        elif pd.isnull(name_value):
            st.session_state.error = True
        else:
            os.mkdir(f"{path}/{name_value}")
            os.mkdir(f"{path}/{name_value}/count")
            os.mkdir(f"{path}/{name_value}/real")
            df = pd.DataFrame(columns=["書櫃", "手工盤點數量"])
            df.to_csv(f"{path}/{name_value}/count/{type_value}.csv", index=False)
            os.mkdir(f"{path}/{name_value}/real/{type_value}")
            df = pd.DataFrame(columns=["default"])
            df.to_csv(f"{path}/{name_value}/real/{type_value}.csv", index=False)



            st.session_state.success = True


def main():
    path =os.getcwd()
    path += "/data"
    # a = os.listdir(path)
    # name = st.selectbox("請選擇講堂...", a)
    # path += f"/{name}"
    # b = os.listdir(path)
    # type = st.selectbox("請選擇講堂...", b)
    # path += f"/{type}"
    # c = os.listdir(path)
    # st.selectbox("請選擇講堂...", c)




    if 'error' not in st.session_state:
        st.session_state.error = False

    if 'success' not in st.session_state:
        st.session_state.success = False
    if 'submit_form' not in st.session_state:
        st.session_state.submit_form = False
    if 'room' not in st.session_state:
        st.session_state.room = ""

    st.title("建立新分區")

    col1, col2 = st.columns(2)
    with col1:
        dir_list = os.listdir(path)
        name = st.selectbox("請選擇講堂...", dir_list + ["新增講堂"])
    with col2:
        if name != "新增講堂":
            path2 = f"{path}/{name}/count"
            type_list = os.listdir(path2)
            type_list = [x.replace(".csv", "") for x in type_list]
        else:
            name = None
            type_list = []
        st.selectbox("請選擇分區...", type_list)

    with st.form("建立新講堂與分區"):
        name_value = st.text_input("講堂名稱", value=name)
        type_value = st.text_input("分區名稱", key="text_key2")

        if st.session_state.submit_form:
            st.form_submit_button("建立講堂與分區", on_click=submit,
                                  args=[True, name_value, type_value, dir_list, type_list])
            st.form_submit_button("取消", on_click=submit, args=[False, name_value, type_value, dir_list, type_list])

        else:
            st.form_submit_button("確認", on_click=submit_comfirm)

    if st.session_state.error:
        st.error("該分區已存在")

    if st.session_state.success:
        st.info("Success")


if __name__ == "__main__":
    main()
