import requests
import json
from pathlib import Path
import time
import random
from headers import headers
import log
from z_stocks.send_msg import push


stocks_json = Path(__file__).parent / "stocks.json"

FILTER_MARKETPLACE = ["CN", "HK"]
PASS_SYMBOLS = [
    "CSI930914",  # 港股通高股息
    "CSIH30590",  # 机器人
]


def get_url(uuid):
    return f"https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?pid=-1&category=1&size=1000&uid={uuid}"


def get_stocks_from_url(url):
    """从雪球API获取最新的股票数据。"""
    try:
        log.info("正在发送请求至雪球 API...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果请求失败则抛出异常
        log.success("请求成功！")
        data = response.json()["data"]["stocks"]
        return data
    except Exception as e:
        log.error(f"从API获取数据时出错: {e}")
        raise


def compare_stocks(old_data, new_data):
    """比较新旧数据，找出差异。"""
    log.info("正在比较数据差异...")

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
        "filtered": {stock["symbol"]: stock for stock in new_data if stock["marketplace"] in FILTER_MARKETPLACE},
    }
    log.success("数据比较完成。")
    return diff


def format_stocks_message(data: dict):
    """根据差异数据格式化要发送的消息。"""
    message = "\n"
    if data["add"]:
        for stock in data["add"].values():
            message += f"    ✅ ADD: {stock['name']} ({stock['symbol']})\n"
    if data["remove"]:
        for stock in data["remove"].values():
            message += f"    ❌ REMOVE: {stock['name']} ({stock['symbol']})\n"

    message += "\n\nCurrent:\n\n"
    for stock in data["filtered"].values():
        if stock["symbol"] in PASS_SYMBOLS:
            continue
        message += f"    {stock['marketplace']: <4}{stock['symbol']: <12}{stock['name']}\n"
    return message


def main():
    error_num = 0
    while True:
        try:
            with stocks_json.open("r", encoding="utf-8") as f:
                data = json.load(f)
            for name, user_data in data.items():
                uuid = user_data["uuid"]
                url = get_url(uuid)
                new_stocks_list = get_stocks_from_url(url)
                compare_data = compare_stocks(user_data["stocks"], new_stocks_list)
                if compare_data["add"] or compare_data["remove"]:
                    log.info("自选有变化")
                    msg = format_stocks_message(compare_data)
                    user_data["stocks"] = new_stocks_list
                    push(f"{name} 自选更新通知", msg, sender="STOCKS")
                    with stocks_json.open("w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                else:
                    log.info("数据无变化")
        except Exception as e:
            error_num += 1
            if error_num >= 10:
                log.error(f"连续失败十次，发送错误报告没，程序暂停 {7200 * 2}s.")
                push("用户自选监控失败", str(e), sender="STOCKS")
                log.exception(e)
                time.sleep(7200 * 2)
            log.exception(e)

        sleep_duration = random.uniform(1, 20)
        log.info("休眠 %.2f 秒, 等待下一轮Tick" % sleep_duration)
        time.sleep(sleep_duration)


if __name__ == "__main__":
    main()
