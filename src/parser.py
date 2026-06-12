from pathlib import Path

from bs4 import BeautifulSoup

from src.normalizer import normalize_item
from src.analyzers.cpu_analyzer import analyze_cpu_title


def get_extra_by_category(part_name, display_name):
    # 依照零件類別取得額外分析資料。
    if part_name == "CPU":
        return analyze_cpu_title(display_name)

    return None


def parse_all_html_files(part_files, html_folder):
    product_list = []

    for part_name in part_files:
        file_name = part_files[part_name]
        file_path = Path(html_folder) / file_name

        if not file_path.exists():
            print("找不到檔案：", file_path)
            continue

        html = file_path.read_text(encoding="utf-8")

        # 使用BeautifulSoup套件解析HTML
        soup = BeautifulSoup(html, "html.parser")

        # 找出HTML中的商品區塊(div class=main區塊中的span標籤)
        product_blocks = soup.select("div.main > span")

        for product_block in product_blocks:
            title_tag = product_block.select_one("div.t")  # div class=t是商品名稱標籤
            price_tag = product_block.select_one("div.x")  # div class=x是價格標籤

            if title_tag is None or price_tag is None:
                continue

            display_name = title_tag.get_text(" ", strip=True)
            price_text = price_tag.get_text(" ", strip=True)

            product = {
                "category": part_name,
                "display_name": display_name,
                "price_text": price_text,
            }

            extra = get_extra_by_category(part_name, display_name)

            if extra is not None:
                product["extra"] = extra

            product = normalize_item(product)
            product_list.append(product)

    return product_list