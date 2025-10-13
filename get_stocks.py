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
COOKIE = "cookiesu=411758851853646; device_id=dd70da9a99c311926daab8b4d833ccfa; Hm_lvt_1db88642e346389874251b5a1eded6e3=1758851854; HMACCOUNT=3F2C01D0E75046DF; smidV2=20250926095734e4bbb374b9b5263ecc09526df307eee10054114a7e14facc0; xq_is_login=1; u=8084764820; s=am11t74ka5; bid=608df1fbdbdaad2d39baaa6ec88568bc_mg0703qh; aliyungf_tc=2f412bbf1c9d23c5acb13fac73be0216513bc73e994876a0ceec184e14830a7e; xq_a_token=063326666234970cbb78d2277025cc05d124db9d; xqat=063326666234970cbb78d2277025cc05d124db9d; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjgwODQ3NjQ4MjAsImlzcyI6InVjIiwiZXhwIjoxNzYyNzQ0MDc2LCJjdG0iOjE3NjAxNTIwNzYzNjEsImNpZCI6ImQ5ZDBuNEFadXAifQ.bWx7jlWCTCIX8V2Rh17ADf-grF1DCywDeFWNwOcmHtfCQxmkRWeTxBPfnuBDyUdtS0ZIsxwgo8XJMfz5VvhCXCZrItmSpCQ_C0rqTtH4ggdOBwkC_Hae-oZKgAWzJ9D-3m9rhmY6rgAGv1g-7sE6Kj4rFldMhfyu9t1NSjLHViv0lg8zmznUPqgGT8rwp5oTB4PpM9nS0o5zvkKIvqg2DQS3w7fTuL8MwrS6SRUlHdR9YpWqcRMvmE27hIdEuMTIoN_kNDrY9uhIQiSBrudU7-tgbfcmbK6IAqkR86YCL1cgQTtwSbFk80bqf30oaqyLDsTKnoS3Lp8eYy-5xU19Sw; xq_r_token=f73f7da919b1873e49db329c540fbb546972328b; acw_tc=b65cfd3417603802370701930e3d7031ae1b8a737d63546ec866e51c4c0b3b; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1760380537; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=qPGXlOJQiMK9B1A10bjohssUS2fPVqWyJW3Vzt2/ZOVHU2WsGrKt8JRIT776mZ5BaqhsiRPCvtsTtgcwwfqksA%3D%3D; ssxmod_itna=1-Wq_x9iPiw4yDhrDgYxBDIxYKGQq7QDOKDl4BtGRRDIkq7=GFDxCgbIB8kmA2DDIL3ZKC2DNoSDEqDsoKxiNDAZ40iDC8ndPxcaW744Qxci4hr_l2mrNpa8QGON5QpjIDYq3NHHZld37UqzLcwOwD0aDmKDU1rb=t4DxaPD5xDTDWeDGDD3axGaDmeDex3mD0bIst8EOtgoD7eDXxGCzCbIDYPDWxDFOzrNx2ONDGHN5yqYGnwxDmbI__BjvBxDn1hAeiiID7v3DlcDsyTIDD5B_yqf__69=Lnm2KdDvxDky4f_zYqvfb3m=keDToDkee4ea7eXgKeA4bixV0D30QK0D3L4eB5eS4bAx5uDbiepEQefmwDD=OiaIePCGreNS1XQpXZ=_e4_dmvk0epWepi_4nqN3nQ3i10wsemxAD3WhmQD3Y2KY_mWWiYxxD; ssxmod_itna2=1-Wq_x9iPiw4yDhrDgYxBDIxYKGQq7QDOKDl4BtGRRDIkq7=GFDxCgbIB8kmA2DDIL3ZKC2DNoSD=4iTwS=fguzFQDGXzeDp62Amt1zr5Xsx5AGbpUi1bAED"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "Host": "stock.xueqiu.com",
    "Referer": "https://xueqiu.com/",
}


SENDER_EMAIL = "donzy.xu@qq.com"
SENDER_EMAIL_KEY = "uixdjqkouqwqcafb"

RECIPIENT = ["donzy.xu@qq.com", "285102896@qq.com"]


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
    sender=SENDER_EMAIL,
    cc_recipients=None,
    auth_code=SENDER_EMAIL_KEY,
):
    recipients_list = [recipient] if isinstance(recipient, str) else recipient
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = formataddr((Header(subject, "utf-8").encode(), sender))
    msg["To"] = formataddr((Header("收件人", "utf-8").encode(), recipient))
    msg["Subject"] = Header(subject, "utf-8")

    # 如果有抄送人，则添加到邮件头
    if cc_recipients:
        msg["Cc"] = ", ".join(cc_recipients)
        recipients_list.extend(cc_recipients)  # 将抄送人也加入到实际发送列表

    try:
        print("Connect to QQ SMTP sever...")
        smtp_server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        print("Login...")
        smtp_server.login(sender, auth_code)
        print("Send mail...")
        smtp_server.sendmail(sender, recipients_list, msg.as_string())
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

        send_qq_mail_notification(subject="STOCKS", body=message, recipient=RECIPIENT[0], cc_recipients=RECIPIENT[1:])
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
        sleep_duration = random.uniform(10, 30)
        print(f"Script finished. Sleeping for {sleep_duration:.2f} seconds...")
        time.sleep(sleep_duration)
