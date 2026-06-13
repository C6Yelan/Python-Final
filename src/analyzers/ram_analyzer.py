import re


def analyze_ram_title(title):
    title = title.strip()

    return {
        "brand": get_ram_brand(title),
        "capacity": get_ram_capacity(title),
        "memory_type": get_ram_memory_type(title),
        "speed": get_ram_speed(title),
        "cl": get_ram_cl(title),
        "module_count": get_ram_module_count(title),
    }


def get_ram_brand(title):
    # RAM通常在第一個空格前是品牌名稱，例如：UMAX 單條16GB
    brand_text = title.split(" ", 1)[0]

    # 有些標題會寫成KLEVV(科賦)，所以只取括號前面的品牌
    if "(" in brand_text:
        brand_text = brand_text.split("(", 1)[0]

    return brand_text


def get_ram_capacity(title):
    result = re.search(r"\d+(GB|G)", title)
    # r表示raw string(原始字串)
    # \d表示數字
    # +表示前面的規則出現一次以上
    # (GB|G)表示數字後面必須接GB或G

    if result is None:
        return None

    capacity_text = result.group(0)
    # group(0)表示回傳整個符合的字串，例如：16GB

    if capacity_text.endswith("GB"):
        return capacity_text
    else:
        return capacity_text.replace("G", "GB")


def get_ram_memory_type(title):
    title = title.upper()

    if "DDR5" in title or "D5" in title:
        return "DDR5"
    elif "DDR4" in title or "D4" in title:
        return "DDR4"
    elif "DDR3" in title or "D3" in title:
        return "DDR3"
    else:
        return None


def get_ram_speed(title):
    result = re.search(r"(DDR3|DDR4|DDR5|D3|D4|D5)[ -]?(\d+)", title, re.IGNORECASE)
    # (DDR3|DDR4|DDR5|D3|D4|D5)表示先找到記憶體類型
    # [ -]?表示中間可以有空白、減號，或完全沒有
    # (\d+)表示抓出後面的頻率數字，例如5600

    if result is None:
        return None

    return int(result.group(2))  # group(1)是記憶體類型，group(2)是頻率數字


def get_ram_cl(title):
    result = re.search(r"CL(\d+)", title, re.IGNORECASE)
    # CL表示從CL開始找
    # (\d+)表示抓出CL後面的數字，例如CL40會抓到40

    if result is None:
        return None

    return int(result.group(1))


def get_ram_module_count(title):
    if "單條" in title:
        return 1
    elif "雙通" in title or "*2" in title:
        return 2
    else:
        return None