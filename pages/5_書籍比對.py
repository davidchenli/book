import csv
import os
import pandas as pd
import streamlit as st

STORAGE_PATH = os.path.join(os.getcwd(), "data", "default", "storage")


def get_file_path(filename):
    return os.path.join(STORAGE_PATH, filename)


def ensure_purchase_file_exists():
    file_path = get_file_path("購買.csv")
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ISBN"])


def purchase():
    isbn = st.session_state.text_key.strip()
    if not isbn:
        return

    ensure_purchase_file_exists()
    file_path = get_file_path("購買.csv")

    with open(file_path, "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([isbn])
        csvfile.flush()

    st.session_state.last_message = f"✅ 已成功購買 ISBN: {isbn}"
    st.session_state.text_key = ""


def cancel():
    st.session_state.text_key = ""


def main():
    st.title("館藏比對與購買系統")

    ensure_purchase_file_exists()

    if "last_message" in st.session_state and st.session_state.last_message:
        st.success(st.session_state.last_message)
        st.session_state.last_message = ""

    st.text_input("請輸入 ISBN 號", key="text_key")

    current_isbn = st.session_state.text_key.strip()

    if current_isbn != "":
        try:
            df_market = pd.read_csv(get_file_path("書單.csv"), dtype={"ISBN": str})
            df_storage = pd.read_csv(get_file_path("館藏.csv"), dtype={"ISBN": str})
            df_foundation = pd.read_csv(get_file_path("基金會.csv"), dtype={"ISBN": str})
            df_purchase = pd.read_csv(get_file_path("購買.csv"), dtype={"ISBN": str})

        except Exception as e:
            st.error(f"讀取資料檔案時發生錯誤：{e}")
            return

        df_market["ISBN"] = df_market["ISBN"].str.strip()
        df_storage["ISBN"] = df_storage["ISBN"].str.strip()
        df_foundation["ISBN"] = df_foundation["ISBN"].str.strip()
        df_purchase["ISBN"] = df_purchase["ISBN"].str.strip()

        df_market_select = df_market[df_market["ISBN"] == current_isbn]
        df_storage_select = df_storage[df_storage["ISBN"] == current_isbn]
        df_foundation_select = df_foundation[df_foundation["ISBN"] == current_isbn]
        df_purchase_select = df_purchase[df_purchase["ISBN"] == current_isbn]

        st.divider()
        st.header("🔍 查詢結果")

        if not df_market_select.empty:
            name = df_market_select["書名"].values[0]
            st.subheader(f"📖 書名：{name}")
            st.dataframe(df_market_select, use_container_width=True)
        else:
            st.warning("查無出版商書單資料")

        if not df_storage_select.empty:
            number = df_storage_select["數量"].values[0]
            st.info(f"🏛️ 館藏現有數量：**{number}** 本")
        else:
            st.info("🏛️ 館藏現有數量：**0** 本（查無館藏資料）")

        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("🛒 已購買數量", len(df_purchase_select))
        with col_stat2:
            if df_foundation_select.empty:
                num = 0
            else:
                num = df_foundation_select["數量"].values[0]
            st.metric("🏢 基金會購買數量", num)

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.button("確認購買", on_click=purchase, type="primary", use_container_width=True)
        with col2:
            st.button("取消", on_click=cancel, use_container_width=True)


if __name__ == "__main__":
    main()
