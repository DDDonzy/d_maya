import cube
import get_stocks

import log

import threading

import time


def main():
    """主函数，用于设置和启动监控线程。"""
    log.info("主程序启动，准备初始化监控线程...")

    # 1. 创建线程列表
    threads = []

    # 2. 创建并配置 cube.main 线程
    cube_thread = threading.Thread(target=cube.main, name="CubeMonitor")
    cube_thread.daemon = True  # 设置为守护线程
    threads.append(cube_thread)

    # 3. 创建并配置 get_stocks.main 线程
    stocks_thread = threading.Thread(target=get_stocks.main, name="StocksMonitor")
    stocks_thread.daemon = True  # 设置为守护线程
    threads.append(stocks_thread)
    # 4. 启动所有线程
    for t in threads:
        log.info(f"正在启动线程: {t.name}")
        t.start()
    # 5. 主线程进入循环，以保持程序运行并监听退出信号
    log.success("所有监控线程已启动，主程序进入等待模式。")

    try:
        while True:
            # 检查线程是否还在运行 (可选，用于监控)
            for t in threads:
                if not t.is_alive():
                    log.error(f"警告！线程 {t.name} 已停止运行！")

            # 主线程休眠，避免空转消耗CPU
            time.sleep(60)

    except KeyboardInterrupt:
        log.warning("检测到 Ctrl+C，程序正在退出...")

    log.info("主程序已退出。")


if __name__ == "__main__":
    main()
