# TW_StkBase

`TW_StkBase` 是一個用於下載股票歷史數據的 Python 程式，使用 [yfinance](https://pypi.org/project/yfinance/) 套件來獲取股票資料，並根據使用者選擇執行增量更新或完整重新下載的功能。

---

## 功能特點

1. **選單功能**：
   
   - 提供使用者選擇更新模式：
     - 增量更新：從上次更新日期到今天。
     - 完整重新下載：下載最近兩年的歷史數據。
     - 退出程式。

2. **設定檔案管理**：
   
   - 自動建立 `config.tw` 設定檔，記錄工作目錄和資料儲存目錄。
   - 確保資料儲存目錄存在。

3. **股票資料下載**：
   
   - 從 `twSTK.csv` 中讀取股票代碼（`ticker` 欄位）。
   - 使用 [yfinance](https://pypi.org/project/yfinance/) 下載股票歷史數據，並以 CSV 格式儲存。

4. **假日判斷**：
   
   - 自動判斷是否為週末或股票市場假日（如元旦、聖誕節），假日無需更新。

---

## 系統需求

- Python 3.7 或以上版本
- 已安裝以下 Python 套件：
  - `yfinance`
  - `pandas`（`yfinance` 依賴此套件）
- 作業系統：Windows、macOS 或 Linux

---

## 安裝與設定

1. **克隆或下載專案**：
   
   ```bash
   git clone https://github.com/parksondow/TW_StkBase.git
   ```

2. **安裝必要套件**：
   使用 `pip` 安裝所需的 Python 套件：
   
   ```bash
   pip install yfinance pandas
   ```

3. **準備 `twSTK.csv` 文件**：
   
   - 在程式的工作目錄下建立 `twSTK.csv` 文件。
   - 文件格式為 CSV，需包含 `ticker` 欄位，例如：
     
     ```csv
     ticker
     AAPL
     MSFT
     TSLA
     ```

---

## 使用方法

1. **執行程式**：
   在終端機中執行以下命令：
   
   ```bash
   python.exe TW_StkBase.py
   ```

2. **選擇更新模式**：
   程式啟動後，會顯示以下選單：
   
   ```
   請選擇更新模式：
   1. 增量更新（從上次更新日期到今天）
   2. 完整重新下載
   3. 退出程式
   請輸入選擇 (1-3):
   ```
   
   - 輸入 `1`：執行增量更新。
   - 輸入 `2`：執行完整重新下載。
   - 輸入 `3`：退出程式。

3. **檢查下載結果**：
   
   - 資料會儲存在 `twstk_data` 資料夾中，檔名為 `<ticker>.csv`。
   - 每個檔案包含該股票的歷史數據。

---

## 程式邏輯

1. **設定檔案與資料夾**：
   
   - 程式會檢查是否存在 `config.tw` 設定檔，若不存在則自動建立。
   - 確保 `twstk_data` 資料夾存在，用於儲存下載的股票數據。

2. **假日判斷**：
   
   - 使用 `is_market_holiday` 函式判斷當天是否為週末或股票市場假日。
   - 若為假日，程式會提示使用者並跳過更新。

3. **增量更新**：
   
   - 讀取現有的股票數據檔案，判斷最後更新日期。
   - 若資料已是最新，則提示使用者無需更新。

4. **完整重新下載**：
   
   - 下載最近兩年的股票歷史數據，覆蓋現有檔案。

5. **錯誤處理**：
   
   - 若 `twSTK.csv` 文件不存在或格式不正確，程式會提示錯誤並返回主選單。
   - 若下載失敗，程式會提示使用者檢查股票代碼。

---

## 文件結構

```
TW_StkBase/
│
├── TW_StkBase.py       # 主程式
├── config.tw           # 設定檔（執行程式後自動生成）
├── twstk_data/         # 儲存股票數據的資料夾（執行程式後自動生成）
└── twSTK.csv           # 股票代碼文件（需手動建立）
```

---

## 注意事項

1. **假日設定**：
   
   - 預設假日為元旦（1 月 1 日）和聖誕節（12 月 25 日）。若需增加假日，可修改 `is_market_holiday` 函式中的 `market_holidays` 列表。

2. **資料來源**：
   
   - 股票數據來源於 [Yahoo Finance](https://finance.yahoo.com/)，下載的數據可能會有延遲或限制。

3. **增量更新限制**：
   
   - 若現有數據檔案格式不正確（如缺少日期欄位），增量更新可能無法正常運作。

---

## 常見問題

### 1. 為什麼程式提示 `twSTK.csv` 不存在？

請確認 `twSTK.csv` 文件已建立，且位於程式的工作目錄中。文件需包含 `ticker` 欄位。

### 2. 為什麼下載的數據為空？

可能的原因：

- 股票代碼（`ticker`）不正確。
- Yahoo Finance 暫時無法提供該股票的數據。

### 3. 如何增加假日？

修改 `is_market_holiday` 函式，將新的假日加入 `market_holidays` 列表。例如：

```python
market_holidays = [
    datetime(date.year, 1, 1),  # 元旦
    datetime(date.year, 12, 25),  # 聖誕節
    datetime(date.year, 2, 28),  # 新增假日
]
```

---

## 授權

此專案採用 MIT 授權，詳見 [LICENSE](LICENSE)。

---

## 聯絡方式

若有任何問題，請聯繫 [parksondow@gmail.com]。


