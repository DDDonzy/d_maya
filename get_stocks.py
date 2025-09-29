import requests
import json
from pathlib import Path

import time
import random

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


STOCKS_JSON = Path(__file__).parent / "stocks.json"


USER_ID = "2292705444"  # 替换为你的雪球用户 ID


PUSH_KEY = "PDU36930TNCh2A1kEt1FD5DwhaZAKPEABDXabM0GI"

URL = f"https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?pid=-1&category=1&size=1000&uid={USER_ID}"
COOKIE = "cookiesu=411758851853646; device_id=dd70da9a99c311926daab8b4d833ccfa; Hm_lvt_1db88642e346389874251b5a1eded6e3=1758851854; HMACCOUNT=3F2C01D0E75046DF; xq_a_token=70cc9666d51ccd7eca3a8cd9b777bc50a6636b27; xqat=70cc9666d51ccd7eca3a8cd9b777bc50a6636b27; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjgwODQ3NjQ4MjAsImlzcyI6InVjIiwiZXhwIjoxNzYxNDQzODY2LCJjdG0iOjE3NTg4NTE4NjY0MDAsImNpZCI6ImQ5ZDBuNEFadXAifQ.AJo1r-aIwOvkg6unS-VQ2HNxR9O2GnHJEdL_05UlaAZuNyzTrRwcyRqPga15UbmFQ5hwcl_fw9x4YLrF_GXnmNHzpZPya6RI433XJ3PTlYz0f6gxK1WlAn4gwfN8ZlPV8ik5k6BEtExS4Sw-phED9QNG4Qf5Mwy9bvAzB6E-nreBAnfRgFuWU2MT52IR7rDyNLn2zSNbmxucpQRjZs6uRLZsvZ1X8HDq3ZqxZc_PkdoeqWnzPZwHWuDCnApHJ2gvmfCggY3YdU1M1vNVmM9G2T_wXXlyF1zHivwn9lW5_sgu2jPfaI5ydzLREUN39lKhaO3hxUiLtB7sytHjt65GOg; xq_r_token=8d09f47d17d2f61210b8b29580d33f99852a9b2a; xq_is_login=1; u=8084764820; s=am11t74ka5; bid=608df1fbdbdaad2d39baaa6ec88568bc_mg0703qh; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1758891876"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "Host": "stock.xueqiu.com",
    "Referer": "https://xueqiu.com/",
}


def dump_stocks_json(new_data, filepath=STOCKS_JSON):
    old_data = []
    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                old_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            old_data = []

    old_symbols = {stock["symbol"] for stock in old_data}
    new_symbols = {stock["symbol"] for stock in new_data}

    added_symbols = new_symbols - old_symbols
    removed_symbols = old_symbols - new_symbols

    added_stocks = {stock["symbol"]: stock for stock in new_data if stock["symbol"] in added_symbols}
    removed_stocks = {stock["symbol"]: stock for stock in old_data if stock["symbol"] in removed_symbols}

    diff = {
        "add": added_stocks,
        "remove": removed_stocks,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

    return diff


def send_telegram_message(
    message,
    bot_token="8104496176:AAElWCT5oagqOUORzq-xlXRxoneC2_4WacQ",
    chat_id="7817871963",
):
    """使用 Telegram Bot 推送"""
    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",  # 可选，支持 Markdown 格式
    }
    try:
        print("正在通过 Telegram 发送通知...")
        response = requests.post(send_url, json=params)
        response.raise_for_status()
        print("Telegram 通知发送成功！")
    except requests.exceptions.RequestException as e:
        print(f"Telegram 通知发送失败: {e}")


def send_qq_mail_notification(
    subject,
    body,
    recipient,
    sender="donzy.xu@qq.com",
    auth_code="uixdjqkouqwqcafb",
):
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = formataddr((Header(subject, "utf-8").encode(), sender))
    msg["To"] = formataddr((Header("收件人", "utf-8").encode(), recipient))
    msg["Subject"] = Header(subject, "utf-8")

    try:
        print("Connect to QQ SMTP sever...")
        smtp_server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        print("Login...")
        smtp_server.login(sender, auth_code)
        print("Send mail...")
        smtp_server.sendmail(sender, [recipient], msg.as_string())
        print("Send success!")

        smtp_server.quit()

    except Exception:
        raise


def get_stocks_json():
    try:
        print("正在发送请求至雪球 API...")
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        print("请求成功！")
        data = response.json()["data"]["stocks"]
        return data

    except Exception:
        raise


def main():
    filter = "CN,HK"

    data = get_stocks_json()
    diff = dump_stocks_json(data)
    message = "\n"
    if diff["add"]:
        for stock in diff["add"].values():
            message += f"    ✅ ADD: {stock['name']} ({stock['symbol']})\n"
    if diff["remove"]:
        for stock in diff["remove"].values():
            message += f"    ❌ REMOVE: {stock['name']} ({stock['symbol']})\n"
    message += "\n\nCurrent:\n\n"
    for stock in data:
        if stock["marketplace"] in filter:
            message += f"    {stock['marketplace']: <4}{stock['symbol']: <12}{stock['name']}\n"

    if diff["add"] or diff["remove"]:
        send_telegram_message(message)

        send_qq_mail_notification(
            subject="STOCKS",
            body=message,
            recipient="donzy.xu@qq.com",
        )
    print(message)


if __name__ == "__main__":
    while True:
        try:
            print(f"[{time.ctime()}] Running the script...")
            main()
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Will retry after the sleep interval.")

        # Generate a random sleep time between 3 and 5 minutes (180 to 300 seconds)
        sleep_duration = random.uniform(180, 300)
        print(f"Script finished. Sleeping for {sleep_duration:.2f} seconds...")
        time.sleep(sleep_duration)