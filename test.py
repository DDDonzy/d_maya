import sys
import re
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser
from PySide2.QtCore import Qt

# ANSI转义序列与HTML对应的样式映射
ansi_to_html = {
    '30': 'color: black;', '31': 'color: red;', '32': 'color: green;', '33': 'color: yellow;',
    '34': 'color: blue;', '35': 'color: magenta;', '36': 'color: cyan;', '37': 'color: white;',
    '40': 'background-color: black;', '41': 'background-color: red;', '42': 'background-color: green;',
    '43': 'background-color: yellow;', '44': 'background-color: blue;', '45': 'background-color: magenta;',
    '46': 'background-color: cyan;', '47': 'background-color: white;',
    '1': 'font-weight: bold;', '4': 'text-decoration: underline;', '7': 'color: white; background-color: black;',
    '0': '',  # Reset
}

# 转换ANSI转义序列为HTML标签
def ansi_to_html_converter(text):
    # 正则表达式匹配ANSI转义序列
    ansi_escape = re.compile(r'\033\[(\d+(?:;\d+)*)m')
    
    # 替换ANSI代码为HTML标签
    def replace_ansi(match):
        codes = match.group(1).split(';')
        style = []
        for code in codes:
            if code in ansi_to_html:
                style.append(ansi_to_html[code])
        # 如果有样式，就将它们放入style属性
        if style:
            return f'<span style="{" ".join(style)}">'
        return ""
    
    # 在字符串中替换ANSI转义序列
    html_text = ansi_escape.sub(replace_ansi, text)
    # 关闭所有HTML标签（重置后）
    html_text = re.sub(r'\033\[0m', '</span>', html_text)
    
    return html_text

# 创建主窗口
window = QWidget()
window.setWindowTitle("ANSI to HTML Example")
window.setGeometry(100, 100, 600, 400)

# 创建布局
layout = QVBoxLayout()

# 创建一个QTextBrowser控件用于显示HTML
text_browser = QTextBrowser()
text_browser.setOpenExternalLinks(True)

# 示例使用
ansi_text = "\033[31mThis is \033[1mbold \033[32mand \033[4munderlined\033[0m text!"
html_output = ansi_to_html_converter(ansi_text)

# 在QTextBrowser中显示HTML输出
text_browser.setHtml(html_output)

# 将控件添加到布局中
layout.addWidget(text_browser)

# 设置布局并显示窗口
window.setLayout(layout)
window.show()
