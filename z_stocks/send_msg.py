import requests
from functools import partial
import log


def send_push_notification(token: str, title: str, message: str, url: str = None, sender: str = None):
    """
    发送推送通知到指定的 API。

    :param token: 接收消息的客户端 token。
    :param title: 推送标题。
    :param message: 推送内容。
    :param url: (可选) 点击通知跳转的链接。
    :param sender: (可选) 发送者名称。
    :return: bool, True 表示成功, False 表示失败。
    """
    api_url = "http://www.ggsuper.com.cn/push/api/v1/sendMsg3_New.php"

    payload = {
        "token": token,
        "title": title,
        "msg": message,
        "issecure": 0,
    }
    # 添加可选参数
    if url:
        payload["url"] = url
    if sender:
        payload["sender"] = sender

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # 如果请求失败 (如 4xx, 5xx), 则抛出异常

        result = response.json()
        if result.get("code") == "80000000" and result.get("msg") == "Success":
            log.success(f"推送成功: {title}")
            return True
        else:
            log.error(f"推送失败: {result}")
            return False

    except requests.exceptions.RequestException as e:
        log.error(f"推送请求异常: {e}")
        return False


push = partial(send_push_notification, "dddonzy9977")
