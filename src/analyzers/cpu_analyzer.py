def analyze_cpu_title(title):
    title = title.strip()

    return {
        "brand": get_cpu_brand(title),
        "model": get_cpu_model(title),
        "core_count": get_cpu_core_count(title),
        "thread_count": get_cpu_thread_count(title),
        "base_clock_ghz": get_cpu_base_clock_ghz(title),
        "max_clock_ghz": get_cpu_max_clock_ghz(title),
    }


def get_cpu_brand(title):
    title = title.lower()  # 將商品標題轉成小寫避免因大小寫造成品牌判斷錯誤

    if "intel" in title:
        return "Intel"
    elif "amd" in title:
        return "AMD"
    else:
        return None


def get_cpu_model(title):
    # CPU標題通常在【之前就是品牌與型號，例如：Intel i5-12400F【6核/12緒】
    if "【" in title:
        title = title.split("【", 1)[0]

    if title.startswith("Intel "):
        title = title.replace("Intel ", "", 1)
    elif title.startswith("AMD "):
        title = title.replace("AMD ", "", 1)

    # CPU標題中常見包裝文字，不屬於型號
    remove_words = [
        "代理盒裝",
        "盒裝",
        "盒",
    ]

    for word in remove_words:
        title = title.removesuffix(word)  # 移除字尾包裝文字

    return title.strip()


def get_cpu_spec_text(title):
    if "【" not in title or "】" not in title:
        return ""

    # 範例：AMD R5 5500GT【6核/12緒】3.6G(↑4.4G)
    spec_text = title.split("【", 1)[1]  # 變成：6核/12緒】3.6G(↑4.4G)
    spec_text = spec_text.split("】", 1)[0]  # 變成：6核/12緒

    return spec_text.strip()


def parse_integer(text):
    # 將核心數、執行緒數等整數規格由text轉成int
    try:
        return int(text)
    except ValueError:
        return text


def parse_float(text):
    # 將CPU頻率等小數規格由text轉成float
    try:
        return float(text)
    except ValueError:
        return text


def get_cpu_core_count(title):
    spec_text = get_cpu_spec_text(title)

    if "核" not in spec_text:
        return None

    core_text = spec_text.split("核", 1)[0].strip()  # 取出核字前方的文字

    return parse_integer(core_text)


def get_cpu_thread_count(title):
    spec_text = get_cpu_spec_text(title)

    if "/" not in spec_text or "緒" not in spec_text:
        return None

    # 取出/和緒之間的文字
    thread_text = spec_text.split("/", 1)[1]
    thread_text = thread_text.split("緒", 1)[0].strip()

    return parse_integer(thread_text)


def get_cpu_base_clock_ghz(title):
    if "】" not in title:
        return None

    clock_text = title.split("】", 1)[1].strip()  # 取出】之後的文字

    if "G" not in clock_text:  # 頻率通常會包含G，若沒有就不像頻率
        return None

    number_text = clock_text.split("G", 1)[0].strip()  # 取出G之前的文字

    return parse_float(number_text)


def get_cpu_max_clock_ghz(title):
    if "↑" not in title:
        return None

    clock_text = title.split("↑", 1)[1].strip()  # 商品標題中用↑符號表示最大頻率

    if "G" not in clock_text:
        return None

    number_text = clock_text.split("G", 1)[0].strip()

    return parse_float(number_text)