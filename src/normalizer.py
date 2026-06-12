def normalize_price(price_text):
    price_text = price_text.replace("開箱討論", "")
    price_text = price_text.replace("Buy", "")
    price_text = price_text.replace("♦", "")
    price_text = price_text.replace("含稅：NT", "")
    price_text = price_text.replace(",", "")
    price_text = price_text.strip()

    return int(price_text)


def normalize_item(product):
    price_text = product.get("price_text", "")

    product["price"] = normalize_price(price_text)

    del product["price_text"]

    return product