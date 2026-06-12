import re


def analyze_storage_title(title):
    title = title.strip()

    return {
        "brand": get_storage_brand(title),
        "model": get_storage_model(title),
        "capacity": get_storage_capacity(title),
        "form_factor": get_storage_form_factor(title),  # 外型規格，例如：2.5吋、M.2
        "interface": get_storage_interface(title),
        "read_speed": get_storage_read_speed(title),
        "write_speed": get_storage_write_speed(title),
        "flash_type": get_storage_flash_type(title),  # 顆粒類型，例如：QLC、TLC、NAND
    }


def get_storage_brand(title):
    # 有些商品標題會把品牌和型號黏在一起，例如：致態小翼e7
    if title.startswith("致態"):
        return "致態"
    
    # 儲存裝置標題在第一個空白前通常是品牌
    return title.split(" ", 1)[0]


def get_capacity_text(title):
    result = re.search(r"\d+(TB|GB|T|G)", title, re.IGNORECASE)
    # r表示raw string(原始字串)
    # \d表示數字
    # +表示前面的規則出現一次以上
    # (TB|GB|T|G)表示數字後面必須接其中一種單位
    # re.IGNORECASE表示搜尋不分大小寫

    if result is None:
        return None

    # group(0)表示回傳整個符合的字串，例如：960G
    # 若直接印出result，會看到搜尋結果物件，例如：<re.Match object; ... match='960G'>
    return result.group(0) 


def get_storage_capacity(title):
    capacity_text = get_capacity_text(title)

    if capacity_text is None:
        return None

    capacity_text = capacity_text.upper()

    if capacity_text.endswith("GB") or capacity_text.endswith("TB"):
        return capacity_text
    elif capacity_text.endswith("G"):
        return capacity_text.replace("G", "GB")
    else:
        return capacity_text.replace("T", "TB")


def get_storage_model(title):
    # 型號大多在品牌後面、容量前面，例如：金士頓 A400 480G → A400
    capacity_text = get_capacity_text(title)
    model_text = title.split(capacity_text, 1)[0]

    brand = get_storage_brand(title)
    model_text = model_text.replace(brand, "", 1)

    return model_text.strip()


def get_storage_form_factor(title):
    title = title.upper()

    if "2.5" in title:
        return "2.5吋"

    # 少數商品有明確寫出M.2短版尺寸
    if "M.2 2230" in title:
        return "M.2 2230"
    elif "M.2 2242" in title:
        return "M.2 2242"
    elif "GEN" in title or "PCIE" in title:  # 若出現PCIe和Gen，通常就是M.2規格
        return "M.2"
    else:
        return None


def get_storage_interface(title):
    title = title.upper()

    if "SATA" in title or "2.5" in title:
        return "SATA"
    elif "PCIE 5.0" in title or "GEN5" in title:
        return "PCIe 5.0"
    elif "PCIE 4.0" in title or "GEN4" in title:
        return "PCIe 4.0"
    elif "PCIE 3.0" in title or "GEN3" in title:
        return "PCIe 3.0"
    else:
        return None


def get_storage_read_speed(title):
    # 從讀520或讀:6000中取出數字
    result = re.search(r"讀:?(\d+)", title)
    # r表示raw string(原始字串)
    # 讀表示從商品標題中的讀這個字開始找
    # :?表示冒號可以出現0次或1次
    # \d表示數字
    # +表示前面的規則出現一次以上
    # ()表示將符合的數字另外分組

    if result is None:
        return None

    return int(result.group(1))


def get_storage_write_speed(title):
    # 從寫450或寫:5000中取出數字
    result = re.search(r"寫:?(\d+)", title)

    if result is None:
        return None

    return int(result.group(1))


def get_storage_flash_type(title):
    title = title.upper()

    if "QLC" in title:
        return "QLC"
    elif "TLC" in title:
        return "TLC"
    elif "NAND" in title:
        return "NAND"
    else:
        return None