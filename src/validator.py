import json
from pathlib import Path

from jsonschema import Draft202012Validator  # Draft202012Validator是jsonschema套件中其中一種驗證器


basic_product_schema = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string"
        },
        "display_name": {
            "type": "string"
        },
        "price": {
            "type": "integer",
            "minimum": 0
        },
    },
    "required": ["category", "display_name", "price"],
    "additionalProperties": False,
}


def load_schema(schema_path):
    # 讀取schemas資料夾中的JSON檔案
    schema_file = Path(schema_path)
    schema_text = schema_file.read_text(encoding="utf-8")

    return json.loads(schema_text)


def get_schema_by_category(category):
    # 根據商品類別決定要用哪一個schema進行驗證
    if category == "CPU":
        return load_schema("schemas/cpu.schema.json")

    if category == "記憶體":
        return load_schema("schemas/ram.schema.json")

    if category == "儲存裝置":
        return load_schema("schemas/storage.schema.json")

    return basic_product_schema


def split_valid_products(products):
    # 接收商品資料，逐一驗證並分成通過與未通過兩類
    valid_products = []
    invalid_products = []

    for product in products:
        category = product.get("category", "")
        schema = get_schema_by_category(category)
        validator = Draft202012Validator(schema)

        if validator.is_valid(product):
            valid_products.append(product)
        else:
            invalid_products.append(product)

    return valid_products, invalid_products