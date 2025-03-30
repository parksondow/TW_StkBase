import os
import csv
import yfinance as yf
from datetime import datetime, timedelta

def is_market_holiday(date):
    """
    判斷是否為假日（週末或股票市場假日）。
    假設股票市場假日為固定日期，可根據實際需求擴展。
    """
    # 判斷是否為週末
    if date.weekday() >= 5:  # 5: 星期六, 6: 星期日
        return True

    # 股票市場假日（可根據實際需求擴展）
    market_holidays = [
        datetime(date.year, 1, 1),  # 元旦
        datetime(date.year, 12, 25),  # 聖誕節
        # 可加入更多假日
    ]
    return date in market_holidays

def display_menu():
    print("""
請選擇更新模式：
1. 增量更新（從上次更新日期到今天）
2. 完整重新下載
3. 退出程式
請輸入選擇 (1-3):
""")
    choice = input().strip()
    return choice

def setup_config():
    config_file = "config.tw"
    work_path = os.getcwd()
    data_path = os.path.join(work_path, "twstk_data")

    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write(f"workPath={work_path}\n")
            f.write(f"dataPath={data_path}\n")

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    return work_path, data_path

def download_stock_data(ticker, data_path, mode):
    file_path = os.path.join(data_path, f"{ticker}.csv")
    if mode == "1":  # 增量更新
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                last_line = f.readlines()[-1]
                last_date = last_line.split(",")[0]
                last_date = datetime.strptime(last_date, "%Y-%m-%d")
                today = datetime.now().date()

                # 判斷是否為假日
                if is_market_holiday(today):
                    print(f"今天是 {today}，股票市場休市，無需更新。")
                    return "no_update"

                if last_date.date() >= today:
                    print(f"{ticker} 的資料已是最新，無需更新。")
                    return "no_update"  # 無需更新，返回主選單

                start_date = last_date + timedelta(days=1)
        else:
            print(f"檔案 {file_path} 不存在，無法進行增量更新，將執行完整下載。")
            mode = "2"
    if mode == "2":  # 完整重新下載
        start_date = datetime.now() - timedelta(days=365 * 2)

    end_date = datetime.now()
    print(f"正在下載 {ticker} 的資料，從 {start_date.date()} 到 {end_date.date()}...")
    data = yf.download(ticker, start=start_date, end=end_date)

    if not data.empty:
        data.to_csv(file_path, mode="a" if mode == "1" else "w", header=mode == "2")
        print(f"{ticker} 的資料已儲存至 {file_path}")
        return "updated"
    else:
        print(f"無法下載 {ticker} 的資料，請檢查代碼是否正確。")
        return "failed"  # 資料下載失敗

def main():
    while True:
        choice = display_menu()
        if choice == "3":
            print("退出程式。")
            break
        elif choice not in ["1", "2"]:
            print("無效的選擇，請重新輸入。")
            continue

        work_path, data_path = setup_config()
        csv_file = os.path.join(work_path, "twSTK.csv")

        if not os.path.exists(csv_file):
            print(f"檔案 {csv_file} 不存在，請確認檔案是否已建立。")
            continue

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if "ticker" not in reader.fieldnames:
                print("無法找到 'ticker' 欄位，請確認 CSV 檔案格式。")
                continue

            for row in reader:
                ticker = row.get("ticker")
                if ticker:
                    result = download_stock_data(ticker, data_path, choice)
                    if result == "no_update":
                        print(f"{ticker} 無需更新，返回主選單。")
                        break
                    elif result == "failed":
                        print(f"{ticker} 資料下載失敗，返回主選單。")
                        break
                else:
                    print("無法找到有效的 'ticker' 值，請確認 CSV 檔案內容。")

if __name__ == "__main__":
    main()