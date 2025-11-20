from os import error
import requests
import log
from pathlib import Path
import json
import datetime
import time
import random
from headers import headers
from send_msg import push


def get_cube_data(cube):
    cube_id = cube.get("cube_id", 0)
    laster_id = cube.get("laster_id", 0)
    rebalancing_history = f"https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol={cube_id}"
    rebalancing_current = f"https://xueqiu.com/cubes/rebalancing/current.json?cube_symbol={cube_id}"

    try:
        response = requests.get(rebalancing_history, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        log.error(e)
        return None

    data = response.json()["list"]
    data.reverse()
    is_changed = False

    msg = ""
    for x in data:
        if x["id"] <= laster_id:
            log.trace("跳过已处理调仓单 {}", x["id"])
            continue
        else:
            log.info("处理调仓单 {}", x["id"])
            update_time = datetime.datetime.fromtimestamp(x["updated_at"] / 1000)
            update_time = update_time.strftime("%Y-%m-%d %H:%M:%S")
            msg += str(update_time) + "\n"
            cube["laster_id"] = x["id"]
            for s in x["rebalancing_histories"]:
                is_changed = True
                stock_name = s.get("stock_name")
                stock_symbol = s.get("stock_symbol")
                weight = s.get("weight") or 0.0
                price = s.get("price") or 0.0
                prev_weight = s.get("prev_weight_adjusted") or 0.0

                name_part = f"{stock_name}({stock_symbol})"
                visual_width = sum(2 if "\u4e00" <= char <= "\u9fff" else 1 for char in name_part)
                padding = 28 - visual_width
                msg += f"    {name_part}{' ' * padding}{prev_weight:>5.2f}% >>> {weight:>5.2f}%，价格:{price:>8.2f} \n"
                log.success(f"    {name_part}{' ' * padding}{prev_weight:>5.2f}% >>> {weight:>5.2f}%，价格:{price:>8.2f}")

    if is_changed:
        is_changed = False
        msg += "=" * 50 + "\n"
        msg += "=" * 50 + "\n"
        msg += "当前持仓 \n"

        response = requests.get(rebalancing_current, headers=headers)
        response.raise_for_status()
        data = response.json()
        for x in data["last_success_rb"]["holdings"]:
            # 格式化持仓行
            name_part = f"{x['stock_name']}({x['stock_symbol']})"
            visual_width = sum(2 if "\u4e00" <= char <= "\u9fff" else 1 for char in name_part)
            padding = 28 - visual_width
            msg += f"    {name_part}{' ' * padding}{x['weight']:>7.2f}% \n"
        # 格式化现金行
        cash_part = "现金"
        cash_visual_width = sum(2 if "\u4e00" <= char <= "\u9fff" else 1 for char in cash_part)
        cash_padding = 28 - cash_visual_width
        msg += f"    {cash_part}{' ' * cash_padding}{data['last_success_rb']['cash']:>7.2f}% \n"
        return msg
    return None


def main():
    error_num = 0
    while True:
        try:
            log.info("开始新的一轮检测")
            cube_json = Path(__file__).parent / r"cube_symbol.json"
            with cube_json.open("r", encoding="utf-8") as f:
                cube_dict = json.load(f)

            for cube_name, cube in cube_dict.items():
                time.sleep(1)
                try:
                    msg = get_cube_data(cube)
                    if msg:
                        push(f"{cube_name} 组合更新", msg, sender="CUBE")
                        with cube_json.open("w", encoding="utf-8") as f:
                            json.dump(cube_dict, f, ensure_ascii=False, indent=4)
                except Exception as e:
                    log.error(e)

            error_num = 0
        except Exception as e:
            error_num += 1
            if error_num >= 10:
                log.error(f"连续失败十次，发送错误报告没，程序暂停 {7200 * 2}s.")
                push("组合监控脚本出错", e, sender="CUBE")
            log.exception(e)

        sleep_duration = random.uniform(1, 20)
        log.info("休眠 %.2f 秒, 等待下一轮Tick" % sleep_duration)
        time.sleep(sleep_duration)


if __name__ == "__main__":
    main()
