def format_products_for_table(products, part_name):
    if part_name == "CPU":
        table = format_cpu_products(products)
    elif part_name == "儲存裝置":
        table = format_storage_products(products)
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
        extra = product.get("extra")  # 取出CPU分析結果

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


def format_storage_products(products):
    table = []

    for product in products:
        extra = product.get("extra")  # 取出儲存裝置分析結果

        table.append(
            {
                "brand": extra.get("brand"),
                "model": extra.get("model"),
                "capacity": extra.get("capacity"),
                "form_factor": extra.get("form_factor"),
                "interface": extra.get("interface"),
                "read_speed": extra.get("read_speed"),
                "write_speed": extra.get("write_speed"),
                "flash_type": extra.get("flash_type"),
                "price": format_price(product.get("price", 0)),
            }
        )

    return table


def format_price(price):
    # 將NT$加入到價格前面，並將數字加上千分位逗號
    return "NT$ " + format(int(price), ",")