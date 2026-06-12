from pathlib import Path

import streamlit as st

from src.parser import parse_all_html_files
from src.table_formatter import format_products_for_table
from src.validator import split_valid_products


# 設定HTML檔案資料夾路徑
html_folder = Path("data/html_files")

# 設定零件類別與對應的HTML檔案
part_files = {
    "CPU": "cpu.html",
    "主機板": "motherboard.html",
    "記憶體": "ram.html",
    "儲存裝置": "storage.html",
    "顯示卡": "gpu.html",
}

# 設定Streamlit網頁標題與版面
st.set_page_config(
    page_title="電腦零件商品資料整理與查詢系統",
    layout="wide",
)

st.title("電腦零件商品資料整理與查詢系統")

# 使用parser.py讀取HTML，並取得商品資料
product_list = parse_all_html_files(part_files, html_folder)

if len(product_list) == 0:
    st.error("沒有讀到商品資料，請確認HTML檔案是否放在data/html_files資料夾中。")
else:
    # 依照零件類別建立頁籤(tab)
    part_names = list(part_files.keys())
    tabs = st.tabs(part_names)

    for index in range(len(part_names)):
        part_name = part_names[index]
        tab = tabs[index]

        with tab:
            # 只保留目前頁籤類別的商品
            current_products = []

            for product in product_list:
                if product["category"] == part_name:
                    current_products.append(product)

            # 驗證目前類別的商品資料
            valid_products, invalid_products = split_valid_products(current_products)

            error_count = 0

            for invalid_product in invalid_products:
                error_count = error_count + len(invalid_product["errors"])

            st.write("讀取商品：" + str(len(current_products)) + " 筆")
            st.write("通過驗證：" + str(len(valid_products)) + " 筆")
            st.write("錯誤商品：" + str(len(invalid_products)) + " 筆")
            st.write("錯誤項目：" + str(error_count) + " 個")

            if len(invalid_products) == 0:
                st.success(part_name + " 資料格式檢查通過。")
            else:
                st.warning(part_name + " 資料格式檢查發現問題，有問題的商品已從正常表格中排除。")

                with st.expander("查看" + part_name + "資料格式錯誤"):
                    for invalid_product in invalid_products:
                        st.write(
                            "第 "
                            + str(invalid_product["index"])
                            + " 筆："
                            + invalid_product["display_name"]
                        )

                        for error_message in invalid_product["errors"]:
                            st.write("- " + error_message)

            if len(valid_products) == 0:
                st.error(part_name + " 沒有任何商品通過資料格式檢查，無法顯示正常商品表格。")
            else:
                # 將通過驗證的商品資料整理成畫面要顯示的表格資料
                display_products = format_products_for_table(valid_products, part_name)

                st.dataframe(
                    display_products,
                    hide_index=True,
                    width="stretch",
                )