def format_products_for_table(products, part_name):
    if part_name == "CPU":
        table = format_cpu_products(products)
    else:
        table = format_basic_products(products)

    return table


def format_basic_products(products):
    # 逐筆建立畫面要顯示的資料，避免修改原本的商品資料
    table = []

    for product in products:
        table.append(
            {
                "display_name": product.get("display_name"),
                "price": format_price(product.get("price", 0)),
            }
        )

    return table


def format_cpu_products(products):
    table = []

    for product in products:
        extra = product.get("extra") # 取出CPU分析結果，後面用來整理CPU詳細欄位

        table.append(
            {
                "brand": extra.get("brand"),
                "model": extra.get("model"),
                "core_count": extra.get("core_count"),
                "thread_count": extra.get("thread_count"),
                "base_clock_ghz": extra.get("base_clock_ghz"),
                "max_clock_ghz": extra.get("max_clock_ghz"),
                "price": format_price(product.get("price", 0)),
            }
        )

    return table


def format_price(price):
    # 將NT$加入到價格前面，並將數字加上千分位逗號
    return "NT$ " + format(int(price), ",")