import json
from pathlib import Path

from jsonschema import Draft202012Validator  # Draft202012Validator是jsonschema套件中其中一種驗證器


basic_product_schema = {  # 暫時性使用，後面會移除
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
    # 讀取schema資料夾中的JSON檔案
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
    # 接收商品資料，逐一驗證並根據結果分為正確與錯誤資料
    valid_products = []
    invalid_products = []

    for index in range(len(products)):
        product = products[index]  # 取出要驗證的商品資料
        category = product.get("category", "")  # 取出商品類別
        schema = get_schema_by_category(category)
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(product))  # 透過iter_errors可收集同商品的多個錯誤

        if len(errors) == 0:
            valid_products.append(product)
        else:
            error_messages = []

            for error in errors:
                # error.json_path是錯誤欄位的位置，error.message是錯誤原因
                error_messages.append(error.json_path + "：" + error.message)

            invalid_products.append(
                {
                    "index": index + 1,
                    "display_name": product.get("display_name", "無商品名稱"),
                    "errors": error_messages,
                }
            )

    return valid_products, invalid_products