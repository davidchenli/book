import os
import pandas as pd
import streamlit as st


def main():
    if "selection" not in st.session_state:
        st.session_state.selection = ""

    base_dir = os.getcwd()
    storage_path = os.path.join(base_dir, "data", "default", "storage")

    purchase_file = os.path.join(storage_path, "購買.csv")
    market_file = os.path.join(storage_path, "書單.csv")

    st.title("購買書籍清單")

    if not os.path.exists(purchase_file) or not os.path.exists(market_file):
        st.error(f"找不到檔案！請確認路徑是否存在：\n{storage_path}")
        return

    try:
        df_purchase = pd.read_csv(purchase_file, dtype=str)
        if "ISBN" not in df_purchase.columns:
            df_purchase = pd.read_csv(purchase_file, header=None, names=["ISBN"], dtype=str)
    except Exception as e:
        st.error(f"讀取購買檔失敗：{e}")
        return

    df_market = pd.read_csv(market_file, dtype={"ISBN": str})

    df_purchase["ISBN"] = df_purchase["ISBN"].astype(str).str.replace(r"[^\d]", "", regex=True)
    df_market["ISBN"] = df_market["ISBN"].astype(str).str.replace(r"[^\d]", "", regex=True)

    df_purchase = df_purchase[df_purchase["ISBN"] != ""]

    if df_purchase.empty:
        st.info("目前無購買書籍紀錄。")
        return

    df_purchase_grouped = df_purchase.groupby("ISBN").size().reset_index(name="總數")
    df_market["價格"] = pd.to_numeric(df_market["價格"], errors="coerce").fillna(0)
    df_purchase_detailed = df_purchase_grouped.merge(df_market, on="ISBN", how="inner")

    if not df_purchase_detailed.empty:
        total = (df_purchase_detailed["總數"] * df_purchase_detailed["價格"]).sum()

        st.metric(label="總購書花費", value=f"${total:,.0f} 元")
        st.subheader("購買書籍詳細清單")
        st.dataframe(df_purchase_detailed, use_container_width=True)

        st.divider()
        st.subheader("🗑️ 刪除購買紀錄")

        options = {
            f"{row['書名']} (ISBN: {row['ISBN']}) - 目前數量: {row['總數']}": row['ISBN']
            for _, row in df_purchase_detailed.iterrows()
        }

        selected_option = st.selectbox("請選擇要刪除的書籍", list(options.keys()))
        selected_isbn = options[selected_option]

        current_count = int(df_purchase_detailed[df_purchase_detailed["ISBN"] == selected_isbn]["總數"].values[0])

        delete_type = st.radio("刪除方式", ["刪除指定數量", "刪除此書全部紀錄"], horizontal=True)

        if delete_type == "刪除指定數量":
            delete_num = st.number_input("刪除數量", min_value=1, max_value=current_count, value=1, step=1)
        else:
            delete_num = current_count

        if st.button("確認刪除", type="primary"):
            match_indices = df_purchase[df_purchase["ISBN"] == selected_isbn].index
            indices_to_drop = match_indices[:delete_num]
            df_purchase = df_purchase.drop(indices_to_drop)

            df_purchase.to_csv(purchase_file, index=False, encoding="utf-8-sig")
            st.success(f"已成功刪除！")
            st.rerun()

        st.divider()

        csv_data = df_purchase_detailed.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="📥 一鍵匯出報表",
            data=csv_data,
            file_name="購買書籍清單.csv",
            mime="text/csv",
        )
    else:
        st.warning("有購買紀錄，但無法在「書單.csv」中對應到對應的 ISBN 資料（請確認書單內容）。")


if __name__ == "__main__":
    main()