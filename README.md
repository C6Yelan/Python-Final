# 電腦零件商品資料整理與查詢系統

本專案為 Python 期末報告使用，主要功能是讀取保存好的原價屋 HTML 檔，整理電腦零件商品名稱、價格與部分規格欄位，並使用 Streamlit 建立簡易查詢介面。

## 安裝方式

### 1. 建立虛擬環境

Windows：

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux：

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. 安裝套件

```bash
pip install -r requirements.txt
```

## 執行方式

```bash
streamlit run app.py
```

執行後，瀏覽器會開啟系統畫面。

## 使用套件

* BeautifulSoup：解析 HTML 商品資料
* jsonschema：檢查資料格式
* Streamlit：建立網頁查詢介面
* pandas：顯示表格資料
* pathlib：處理檔案路徑
* re：分析商品名稱中的規格文字

## 資料來源說明

本系統使用事先保存好的原價屋 HTML 檔，不做即時爬蟲。

## 功能簡介

* 讀取 HTML 商品資料
* 擷取商品名稱與價格
* 依照零件類別整理商品
* CPU、記憶體、儲存裝置進行規格欄位分析
* 使用 JSON Schema 檢查資料格式
* 提供商品名稱搜尋與類別頁籤展示