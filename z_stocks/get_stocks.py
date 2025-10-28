import requests
import json
from pathlib import Path

import time
import random

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


class StocksHandle:
    """
    负责所有与股票数据相关的操作：
    1. 从API获取最新数据
    2. 读/写本地缓存文件
    3. 比较数据差异
    """

    # 本地储存文件路径
    STOCKS_JSON = Path(__file__).parent / "stocks.json"

    USER_ID = "2292705444"  # 替换为你的雪球用户 ID
    URL = f"https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?pid=-1&category=1&size=1000&uid={USER_ID}"  # 雪球用户URL
    COOKIE = "cookiesu=411758851853646; device_id=dd70da9a99c311926daab8b4d833ccfa; Hm_lvt_1db88642e346389874251b5a1eded6e3=1758851854; HMACCOUNT=3F2C01D0E75046DF; smidV2=20250926095734e4bbb374b9b5263ecc09526df307eee10054114a7e14facc0; xq_is_login=1; u=8084764820; s=am11t74ka5; bid=608df1fbdbdaad2d39baaa6ec88568bc_mg0703qh; aliyungf_tc=2f412bbf1c9d23c5acb13fac73be0216513bc73e994876a0ceec184e14830a7e; xq_a_token=063326666234970cbb78d2277025cc05d124db9d; xqat=063326666234970cbb78d2277025cc05d124db9d; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjgwODQ3NjQ4MjAsImlzcyI6InVjIiwiZXhwIjoxNzYyNzQ0MDc2LCJjdG0iOjE3NjAxNTIwNzYzNjEsImNpZCI6ImQ5ZDBuNEFadXAifQ.bWx7jlWCTCIX8V2Rh17ADf-grF1DCywDeFWNwOcmHtfCQxmkRWeTxBPfnuBDyUdtS0ZIsxwgo8XJMfz5VvhCXCZrItmSpCQ_C0rqTtH4ggdOBwkC_Hae-oZKgAWzJ9D-3m9rhmY6rgAGv1g-7sE6Kj4rFldMhfyu9t1NSjLHViv0lg8zmznUPqgGT8rwp5oTB4PpM9nS0o5zvkKIvqg2DQS3w7fTuL8MwrS6SRUlHdR9YpWqcRMvmE27hIdEuMTIoN_kNDrY9uhIQiSBrudU7-tgbfcmbK6IAqkR86YCL1cgQTtwSbFk80bqf30oaqyLDsTKnoS3Lp8eYy-5xU19Sw; xq_r_token=f73f7da919b1873e49db329c540fbb546972328b; acw_tc=b65cfd3417603802370701930e3d7031ae1b8a737d63546ec866e51c4c0b3b; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1760380537; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=qPGXlOJQiMK9B1A10bjohssUS2fPVqWyJW3Vzt2/ZOVHU2WsGrKt8JRIT776mZ5BaqhsiRPCvtsTtgcwwfqksA%3D%3D; ssxmod_itna=1-Wq_x9iPiw4yDhrDgYxBDIxYKGQq7QDOKDl4BtGRRDIkq7=GFDxCgbIB8kmA2DDIL3ZKC2DNoSDEqDsoKxiNDAZ40iDC8ndPxcaW744Qxci4hr_l2mrNpa8QGON5QpjIDYq3NHHZld37UqzLcwOwD0aDmKDU1rb=t4DxaPD5xDTDWeDGDD3axGaDmeDex3mD0bIst8EOtgoD7eDXxGCzCbIDYPDWxDFOzrNx2ONDGHN5yqYGnwxDmbI__BjvBxDn1hAeiiID7v3DlcDsyTIDD5B_yqf__69=Lnm2KdDvxDky4f_zYqvfb3m=keDToDkee4ea7eXgKeA4bixV0D30QK0D3L4eB5eS4bAx5uDbiepEQefmwDD=OiaIePCGreNS1XQpXZ=_e4_dmvk0epWepi_4nqN3nQ3i10wsemxAD3WhmQD3Y2KY_mWWiYxxD; ssxmod_itna2=1-Wq_x9iPiw4yDhrDgYxBDIxYKGQq7QDOKDl4BtGRRDIkq7=GFDxCgbIB8kmA2DDIL3ZKC2DNoSD=4iTwS=fguzFQDGXzeDp62Amt1zr5Xsx5AGbpUi1bAED"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Cookie": COOKIE,
        "Host": "stock.xueqiu.com",
        "Referer": "https://xueqiu.com/",
    }
    FILTER = ["CN", "HK"]
    PASS = [
        "CSI930914",  # 港股通高股息
        "CSIH30590",  # 机器人
    ]

    def get_stocks_from_url(self):
        try:
            print("正在发送请求至雪球 API...")
            response = requests.get(self.URL, headers=self.HEADERS, timeout=10)
            response.raise_for_status()
            print("请求成功！")
            data = response.json()["data"]["stocks"]
            return data

        except Exception:
            raise

    def compare_stocks(self, new_data):
        print("正在比较数据差异...")
        if self.STOCKS_JSON.exists():
            try:
                with open(self.STOCKS_JSON, "r", encoding="utf-8") as f:
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
            "current": new_data,
            "filtered": {stock["symbol"]: stock for stock in new_data if stock["marketplace"] in self.FILTER},
        }

        # with open(self.STOCKS_JSON, "w", encoding="utf-8") as f:
        #     json.dump(new_data, f, ensure_ascii=False, indent=4)
        print("数据比较完成。")
        return diff

    def stocks_message(self, data: dict):
        message = "\n"
        if data["add"]:
            for stock in data["add"].values():
                message += f"    ✅ ADD: {stock['name']} ({stock['symbol']})\n"
        if data["remove"]:
            for stock in data["remove"].values():
                message += f"    ❌ REMOVE: {stock['name']} ({stock['symbol']})\n"
        message += "\n\nCurrent:\n\n"
        for stock in data["filtered"].values():
            if stock["symbol"] in self.PASS:
                continue
            message += f"    {stock['marketplace']: <4}{stock['symbol']: <12}{stock['name']}\n"
        return message


class SenderHandle:
    # qq Mail
    SENDER_EMAIL = "donzy.xu@qq.com"  # 发件邮箱
    SENDER_EMAIL_KEY = "uixdjqkouqwqcafb"  # 发件邮箱授权码
    RECIPIENT = [
        "donzy.xu@qq.com",
    ]  # 收件邮箱列表 #"285102896@qq.com"
    # telegram Bot
    BOT_TOKEN = "8104496176:AAElWCT5oagqOUORzq-xlXRxoneC2_4WacQ"
    CHAT_ID = "7817871963"

    def send_telegram_message(self, message):
        """使用 Telegram Bot 推送"""
        print("正在通过 Telegram 发送通知...")
        send_url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": self.CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",  # 可选，支持 Markdown 格式
        }
        try:
            response = requests.post(send_url, json=params)
            response.raise_for_status()
            print("Telegram 通知发送成功！")
        except Exception:
            print("Telegram 通知发送失败")
            raise

    def send_qqMail_message(self, message, subject="股票监控通知"):
        print("正在通过 QQ 邮箱 发送通知...")
        recipients_list = [self.RECIPIENT[0]] if isinstance(self.RECIPIENT[0], str) else self.RECIPIENT[0]
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = formataddr((Header(subject, "utf-8").encode(), self.SENDER_EMAIL))
        msg["To"] = formataddr((Header("收件人", "utf-8").encode(), self.RECIPIENT[0]))

        msg["Cc"] = ", ".join(self.RECIPIENT[1:])  # 如果有抄送人，则添加到邮件头
        recipients_list.extend(self.RECIPIENT[1:])  # 将抄送人也加入到实际发送列表

        try:
            smtp_server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            smtp_server.login(self.SENDER_EMAIL, self.SENDER_EMAIL_KEY)
            smtp_server.sendmail(self.SENDER_EMAIL, recipients_list, msg.as_string())
            smtp_server.quit()
            print("QQ 邮箱 通知发送成功！")
        except Exception:
            print("QQ 邮箱 通知发送失败! ")
            raise


def main():
    send_error = True
    stocks_handle = StocksHandle()
    sender_stocks_handle = SenderHandle()
    while True:
        print("\n" * 2)
        print("开始新一轮检测...")
        try:
            data = stocks_handle.get_stocks_from_url()
            compare_data = stocks_handle.compare_stocks(data)
            message = stocks_handle.stocks_message(compare_data)
            print(message)

            if compare_data["add"] or compare_data["remove"]:
                print("检测到数据变更，正在发送通知...")
                sender_stocks_handle.send_qqMail_message(message)
                sender_stocks_handle.send_telegram_message(message)

                with open(stocks_handle.STOCKS_JSON, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print("本地缓存已更新。")
            else:
                print("本轮检测未发现数据变更。")

            send_error = True  # 解除错误通知锁定

        except Exception as e:
            print("本轮检测失败，等待下次重试...")
            print(e)
            try:
                if send_error is True:
                    sender_stocks_handle.send_qqMail_message(subject="股票监控通知出错", message=f"股票监控脚本运行出错，请检查！\n-\n {e}")
                    sender_stocks_handle.send_telegram_message(message=f"股票监控脚本运行出错，请检查！\n-\n {e}")
                    send_error = False  # 保证只发送一次错误通知，防止频繁报错时刷屏。
            except Exception as ee:
                print(ee)

        sleep_duration = random.uniform(5, 25)
        print("休眠 %.2f 秒, 等待下一轮Tick" % sleep_duration)
        time.sleep(sleep_duration)


if __name__ == "__main__":
    main()
