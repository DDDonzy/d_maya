import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


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


# 调用函数发送通知
send_qq_mail_notification(
    subject="STOCKS MESSAGE",
    body="这是一个来自你的Python监控脚本的通知。\n\n✅ 新增自选: 阿里巴巴 (BABA)",
    recipient="donzy.xu@qq.com",
)
