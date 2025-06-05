# -*- coding: utf-8 -*-
"""
SVG图标处理工具集

本脚本包含以下功能：
1. 修复SVG文件以便在Qt Designer中正确显示颜色（主要通过内联CSS样式）。
2. 直接修改SVG文件中图形元素的颜色属性（如fill, stroke, stop-color），
   并应用HSV（色相、饱和度、明度）色彩调整。
3. 批量处理指定目录下的所有SVG文件，生成颜色调整后的不同状态版本（如hover, pressed, normal）。

主要函数:
- repair_svg_for_qt: 修复SVG以便在Qt Designer中使用。
- set_svg_colors_directly_hsv: 直接修改SVG颜色属性并应用HSV调整。
- find_all_svg_files: 查找目录下的所有SVG文件。

使用方法:
- 根据需要在 if __name__ == '__main__': 代码块中配置源目录和输出目录。
- 脚本依赖第三方库 'cssutils'，请确保已安装 (pip install cssutils)。
"""

import xml.etree.ElementTree as ET
import os
import re  # 用于颜色解析
import colorsys  # 用于RGB <-> HSV转换
import logging # 用于cssutils日志配置
import cssutils  # 用于解析CSS样式 (你需要 pip install cssutils)

# --- 全局常量 ---
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
# XLINK_NAMESPACE = "http://www.w3.org/1999/xlink" # 如果将来需要处理xlink属性，可以取消注释

NAMED_COLORS = {
    "aliceblue": "#f0f8ff", "antiquewhite": "#faebd7", "aqua": "#00ffff", "aquamarine": "#7fffd4", "azure": "#f0ffff",
    "beige": "#f5f5dc", "bisque": "#ffe4c4", "black": "#000000", "blanchedalmond": "#ffebcd", "blue": "#0000ff",
    "blueviolet": "#8a2be2", "brown": "#a52a2a", "burlywood": "#deb887", "cadetblue": "#5f9ea0", "chartreuse": "#7fff00",
    "chocolate": "#d2691e", "coral": "#ff7f50", "cornflowerblue": "#6495ed", "cornsilk": "#fff8dc", "crimson": "#dc143c",
    "cyan": "#00ffff", "darkblue": "#00008b", "darkcyan": "#008b8b", "darkgoldenrod": "#b8860b", "darkgray": "#a9a9a9",
    "darkgrey": "#a9a9a9", "darkgreen": "#006400", "darkkhaki": "#bdb76b", "darkmagenta": "#8b008b", "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00", "darkorchid": "#9932cc", "darkred": "#8b0000", "darksalmon": "#e9967a", "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b", "darkslategray": "#2f4f4f", "darkslategrey": "#2f4f4f", "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3", "deeppink": "#ff1493", "deepskyblue": "#00bfff", "dimgray": "#696969", "dimgrey": "#696969",
    "dodgerblue": "#1e90ff", "firebrick": "#b22222", "floralwhite": "#fffaf0", "forestgreen": "#228b22", "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc", "ghostwhite": "#f8f8ff", "gold": "#ffd700", "goldenrod": "#daa520", "gray": "#808080",
    "grey": "#808080", "green": "#008000", "greenyellow": "#adff2f", "honeydew": "#f0fff0", "hotpink": "#ff69b4",
    "indianred": "#cd5c5c", "indigo": "#4b0082", "ivory": "#fffff0", "khaki": "#f0e68c", "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5", "lawngreen": "#7cfc00", "lemonchiffon": "#fffacd", "lightblue": "#add8e6", "lightcoral": "#f08080",
    "lightcyan": "#e0ffff", "lightgoldenrodyellow": "#fafad2", "lightgray": "#d3d3d3", "lightgrey": "#d3d3d3",
    "lightgreen": "#90ee90", "lightpink": "#ffb6c1", "lightsalmon": "#ffa07a", "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa", "lightslategray": "#778899", "lightslategrey": "#778899", "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0", "lime": "#00ff00", "limegreen": "#32cd32", "linen": "#faf0e6", "magenta": "#ff00ff",
    "maroon": "#800000", "mediumaquamarine": "#66cdaa", "mediumblue": "#0000cd", "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db", "mediumseagreen": "#3cb371", "mediumslateblue": "#7b68ee", "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc", "mediumvioletred": "#c71585", "midnightblue": "#191970", "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1", "moccasin": "#ffe4b5", "navajowhite": "#ffdead", "navy": "#000080", "oldlace": "#fdf5e6",
    "olive": "#808000", "olivedrab": "#6b8e23", "orange": "#ffa500", "orangered": "#ff4500", "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa", "palegreen": "#98fb98", "paleturquoise": "#afeeee", "palevioletred": "#db7093",
    "papayawhip": "#ffefd5", "peachpuff": "#ffdab9", "peru": "#cd853f", "pink": "#ffc0cb", "plum": "#dda0dd",
    "powderblue": "#b0e0e6", "purple": "#800080", "rebeccapurple": "#663399", "red": "#ff0000", "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1", "saddlebrown": "#8b4513", "salmon": "#fa8072", "sandybrown": "#f4a460", "seagreen": "#2e8b57",
    "seashell": "#fff5ee", "sienna": "#a0522d", "silver": "#c0c0c0", "skyblue": "#87ceeb", "slateblue": "#6a5acd",
    "slategray": "#708090", "slategrey": "#708090", "snow": "#fffafa", "springgreen": "#00ff7f", "steelblue": "#4682b4",
    "tan": "#d2b48c", "teal": "#008080", "thistle": "#d8bfd8", "tomato": "#ff6347", "turquoise": "#40e0d0",
    "violet": "#ee82ee", "wheat": "#f5deb3", "white": "#ffffff", "whitesmoke": "#f5f5f5", "yellow": "#ffff00",
    "yellowgreen": "#9acd32"
}

# --- Logging Configuration ---
# 配置cssutils的日志级别，避免在控制台打印过多不必要的警告信息
cssutils.log.setLevel(logging.CRITICAL)  # 通常只显示严重错误


# --- 辅助函数 ---

def _parse_color_string_to_rgba(color_str: str):
    """
    解析常见的颜色字符串 (如十六进制码、rgb()、rgba()函数式以及英文颜色名)
    并将其转换为一个包含 (r, g, b, alpha) 值的元组。

    Args:
        color_str (str): 输入的颜色字符串。

    Returns:
        tuple: (r, g, b, alpha)
               r, g, b 的范围是 0-255。
               alpha (透明度) 的范围是 0.0-1.0。
               如果颜色是 'none', 'transparent', 'currentColor', 'hsl_unsupported' (暂不支持的hsl格式)
               或者无法解析，则r分量会返回特殊字符串标记或None，其余分量可能为None或0.0。
    """
    if not color_str or not isinstance(color_str, str):
        return None, None, None, 0.0 # 输入无效

    color_str = color_str.lower().strip()

    if color_str == "none" or color_str == "transparent":
        return None, None, None, 0.0 # 'none' 或 'transparent' 表示无颜色或全透明
    if color_str == "currentcolor":
        return "currentColor", None, None, 0.0  # 特殊标记，表示使用当前文本颜色，不在此处解析
    if color_str.startswith("hsl"): # HSL/HSLA 颜色暂不完整支持转换
        return "hsl_unsupported", None, None, 0.0 # 特殊标记

    # 检查是否为已定义的颜色名
    if color_str in NAMED_COLORS:
        color_str = NAMED_COLORS[color_str] # 将颜色名替换为其对应的十六进制码

    # 解析十六进制颜色码: #RRGGBB 或 #RGB
    if color_str.startswith("#"):
        hex_color = color_str[1:]
        if len(hex_color) == 6: # #RRGGBB
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return r, g, b, 1.0 # 十六进制码默认不透明
        elif len(hex_color) == 3: # #RGB (简写形式)
            r = int(hex_color[0] * 2, 16) # 例如 "f" -> "ff"
            g = int(hex_color[1] * 2, 16)
            b = int(hex_color[2] * 2, 16)
            return r, g, b, 1.0 # 十六进制码默认不透明
        else: # 无效的十六进制码长度
            return None, None, None, 0.0


    # 解析 rgb(r,g,b) 函数式颜色
    match_rgb = re.match(r"rgb\((\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\)", color_str)
    if match_rgb:
        r, g, b = [int(c) for c in match_rgb.groups()]
        # 校验RGB值范围
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            return None, None, None, 0.0 # RGB值超出范围
        return r, g, b, 1.0 # rgb() 默认不透明

    # 解析 rgba(r,g,b,a) 函数式颜色
    match_rgba = re.match(r"rgba\((\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*([0-9.]+)\)", color_str)
    if match_rgba:
        r, g, b = [int(c) for c in match_rgba.groups()[:3]]
        a = float(match_rgba.groups()[3])
        # 校验RGB值范围和Alpha值范围
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255 and 0.0 <= a <= 1.0):
            return None, None, None, 0.0 # RGBA值超出范围
        return r, g, b, a

    # 如果以上都未匹配，则认为无法解析
    return None, None, None, 0.0


def _rgb_to_hsv(r, g, b):
    """
    将RGB颜色值转换为HSV颜色值。

    Args:
        r (int/float): 红色分量 (0-255)。
        g (int/float): 绿色分量 (0-255)。
        b (int/float): 蓝色分量 (0-255)。

    Returns:
        tuple: (h, s, v)
               h (色相) 范围: 0-360。
               s (饱和度) 范围: 0.0-1.0。
               v (明度) 范围: 0.0-1.0。
    """
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    return h * 360.0, s, v


def _hsv_to_rgb(h, s, v):
    """
    将HSV颜色值转换为RGB颜色值。

    Args:
        h (float): 色相 (0-360)。
        s (float): 饱和度 (0.0-1.0)。
        v (float): 明度 (0.0-1.0)。

    Returns:
        tuple: (r, g, b)
               r, g, b (红,绿,蓝分量) 范围: 0-255。
    """
    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return r * 255.0, g * 255.0, b * 255.0


def get_element_local_name(element):
    """
    获取SVG元素的本地名称 (即去除命名空间前缀的标签名)。

    Args:
        element (xml.etree.ElementTree.Element): SVG元素。

    Returns:
        str: 元素的本地名称。
    """
    return element.tag.split('}')[-1] if '}' in element.tag else element.tag


def find_all_svg_files(directory: str):
    """
    递归查找指定目录及其所有子目录下的全部 .svg 文件。

    Args:
        directory (str): 要搜索的根目录路径。

    Returns:
        list: 包含所有找到的SVG文件完整路径的列表。
    """
    svg_files = []
    print(f"🔍 正在从目录 '{directory}' 中查找SVG文件...")
    for root_dir, _, files_in_dir in os.walk(directory):
        for file_name in files_in_dir:
            if file_name.lower().endswith('.svg'):
                svg_files.append(os.path.join(root_dir, file_name))
    return svg_files


# --- 主要SVG处理函数 ---

def repair_svg_for_qt(input_svg_path: str, output_svg_path: str):
    """
    尝试修复SVG文件，以便在Qt Designer等工具中能更准确地显示颜色。
    主要操作是将定义在 <style> 标签内的CSS样式内联到各个SVG元素上作为它们的直接属性，
    并移除原有的 <style> 标签和元素上的 class 属性。

    Args:
        input_svg_path (str): 输入的原始SVG文件路径。
        output_svg_path (str): 修复后输出的SVG文件路径。
    """
    print(f"🚀 开始修复SVG文件以兼容Qt: {input_svg_path}")

    output_directory = os.path.dirname(output_svg_path)
    if output_directory and not os.path.exists(output_directory): # 确保输出目录存在
        os.makedirs(output_directory)
        print(f"  创建输出目录 (如果需要): {output_directory}")

    try:
        # 注册SVG命名空间，以便在输出XML时使用默认命名空间而不是 ns0: 前缀
        ET.register_namespace('', SVG_NAMESPACE)
        # ET.register_namespace('xlink', XLINK_NAMESPACE) # 如果处理xlink属性可取消注释

        tree = ET.parse(input_svg_path)
        root = tree.getroot()

        all_styles_content = ""
        style_elements_to_remove = []

        # 步骤 1: 收集所有 <style> 标签的内容，并标记待删除
        for style_element in root.findall(f".//{{{SVG_NAMESPACE}}}style"): # 查找所有style标签
            if style_element.text:
                all_styles_content += style_element.text + "\n"
            style_elements_to_remove.append(style_element)

        # 从XML树中移除 <style> 标签 (必须在迭代查找父元素之前完成收集)
        for style_el_to_remove in style_elements_to_remove:
            # 查找其父元素以进行安全移除
            parent_map = {c: p for p in root.iter() for c in p} # 构建子到父的映射
            parent_of_style = parent_map.get(style_el_to_remove)
            if parent_of_style is not None:
                parent_of_style.remove(style_el_to_remove)
            elif root == style_el_to_remove: # 理论上style不应是根，但以防万一
                 print(f"  警告: <style> 标签是根元素，无法移除。路径: {input_svg_path}")


        if not all_styles_content.strip():
            print(f"  ℹ️ 文件 '{os.path.basename(input_svg_path)}' 中未找到 <style> 标签内容。主要进行class属性移除。")
        
        # 步骤 2: 使用cssutils解析收集到的CSS样式文本
        # cssutils会处理CSS的解析，包括错误处理
        stylesheet = cssutils.parseString(all_styles_content)

        # 步骤 3: 遍历所有SVG元素，将解析出的CSS样式应用为元素的直接属性
        elements_in_tree = list(root.iter())  # 获取树中所有元素

        for element in elements_in_tree:
            # 确保是有效元素节点 (跳过注释、处理指令等)
            if not isinstance(element.tag, str) or '}' not in element.tag:
                continue

            element_local_name = get_element_local_name(element)
            element_id = element.get('id')
            element_classes = element.get('class', '').split()

            # 遍历样式表中的每一条规则
            for rule in stylesheet.cssRules:
                if rule.type == rule.STYLE_RULE: # 只处理样式规则 (如 'selector { prop: value; }')
                    # 一条规则可能对应多个选择器 (如 'h1, h2 { color: blue; }')
                    # cssutils的 rule.selectorText 是一个字符串，可能包含逗号
                    # 对于更准确的匹配，应该使用 rule.selectorList
                    for selector in rule.selectorList: # selector 是一个 CSSSelector 对象
                        selector_text = selector.selectorText.strip()
                        
                        # 进行选择器匹配 (这是一个简化的匹配逻辑)
                        matched_by_selector = False
                        if selector_text == element_local_name:  # 标签名选择器 (e.g., "rect")
                            matched_by_selector = True
                        elif selector_text.startswith('.') and selector_text[1:] in element_classes:  # 类选择器 (e.g., ".myclass")
                            matched_by_selector = True
                        elif selector_text.startswith('#') and selector_text[1:] == element_id:  # ID 选择器 (e.g., "#myid")
                            matched_by_selector = True
                        elif selector_text == "*": # 通用选择器
                            matched_by_selector = True
                        
                        # 如果当前元素匹配此CSS选择器
                        if matched_by_selector:
                            # 将此规则下的所有样式声明应用到元素上
                            for css_property in rule.style: # css_property 是一个 CSSProperty 对象
                                # prop.name 是CSS属性名 (如 'fill', 'stroke-width')
                                # prop.value 是CSS属性值 (如 'red', '2px')
                                # 直接用 element.set() 会覆盖已有的同名直接属性
                                element.set(css_property.name, css_property.value)
                                # print(f"    内联样式到 <{element_local_name}>: {css_property.name} = {css_property.value}")

        # 步骤 4: 移除所有元素上的 class 属性 (因为相关样式已内联)
        for element in elements_in_tree:
            if isinstance(element.tag, str) and '}' in element.tag: # 再次确保是元素
                 if 'class' in element.attrib:
                    del element.attrib['class']
        
        # 步骤 5: (可选优化) 移除因此变为空的 <defs> 标签
        # 这部分逻辑可以根据需要保留或移除，空defs通常无害
        defs_tags = list(root.findall(f".//{{{SVG_NAMESPACE}}}defs")) # 找到所有defs
        for defs_element in defs_tags:
            if not list(defs_element) and not (defs_element.text and defs_element.text.strip()):
                # print(f"  ℹ️ 移除了一个空的 <defs> 标签。")
                parent_map = {c: p for p in root.iter() for c in p}
                parent_of_defs = parent_map.get(defs_element)
                if parent_of_defs is not None:
                    parent_of_defs.remove(defs_element)

        # 步骤 6: 写入修复后的SVG文件
        tree.write(output_svg_path, encoding="utf-8", xml_declaration=True)
        print(f"  ✅ SVG文件修复完成: {output_svg_path}")
        # print("     请在Qt Designer中测试修复后的文件。")

    except ET.ParseError as e:
        print(f"  😭 解析SVG文件 '{input_svg_path}' 出错: {e}")
    except ImportError: # 特别处理cssutils未安装的情况
        print("  😭 关键错误: Python库 'cssutils' 未安装。请运行 'pip install cssutils' 来安装它。")
        print("     修复功能无法执行。")
        return # 中断此函数的执行
    except Exception as e:
        print(f"  😭 处理SVG '{input_svg_path}' 时发生未知错误: {e}")


def set_svg_colors_directly_hsv(input_svg_path: str,
                                output_svg_path: str,
                                hue_rotate_degrees: float = 0.0,
                                saturation_factor: float = 1.0,
                                value_factor: float = 1.0):
    """
    直接修改SVG文件中图形元素的颜色属性（如 `fill`, `stroke`, `stop-color`），
    并应用HSV（色相、饱和度、明度）色彩调整。
    此方法旨在确保颜色变化在Qt Designer等环境中能够正确显示。
    颜色调整顺序为：色相 -> 饱和度 -> 明度。

    Args:
        input_svg_path (str): 输入的原始SVG文件路径。
                              建议此SVG已通过 `repair_svg_for_qt` 处理，以确保颜色属性是直接的。
        output_svg_path (str): 处理后输出的SVG文件路径。
        hue_rotate_degrees (float, optional): 色相旋转的角度值 (0-360)。默认为 0.0 (无变化)。
        saturation_factor (float, optional): 饱和度调整因子。默认为 1.0 (无变化)。
                                             0.0 表示完全去饱和 (灰度图)。
                                             0.5 表示饱和度降低50%。
                                             1.5 表示饱和度增加50%。
        value_factor (float, optional): 明度(亮度)调整因子。默认为 1.0 (无变化)。
                                        0.8 表示亮度降低20%。
                                        1.2 表示亮度增加20%。
    """
    print(f"🎨 开始直接修改SVG颜色属性并应用HSV调整: {os.path.basename(input_svg_path)}")
    output_directory = os.path.dirname(output_svg_path)
    if output_directory and not os.path.exists(output_directory): # 确保输出目录存在
        os.makedirs(output_directory)
        # print(f"  创建输出目录 (如果需要): {output_directory}")

    if not os.path.splitext(input_svg_path)[1].lower() == ".svg":
        print(f"  错误: 输入文件 '{input_svg_path}' 不是一个SVG文件。")
        return

    try:
        ET.register_namespace('', SVG_NAMESPACE) # 注册默认命名空间
    except AttributeError:
        # 旧版Python的ElementTree可能不支持全局register_namespace
        pass

    try:
        tree = ET.parse(input_svg_path)
        root = tree.getroot()

        # 定义需要查找和修改颜色值的SVG属性列表
        color_attributes_to_modify = ['fill', 'stroke', 'stop-color']
        # 未来可考虑扩展到如 'flood-color', 'lighting-color' 等，但它们通常用于滤镜元素

        # 检查是否真的需要进行颜色处理 (如果所有调整参数都是默认值，则不进行颜色修改)
        needs_color_processing = not (abs(hue_rotate_degrees) < 1e-6 and \
                                      abs(saturation_factor - 1.0) < 1e-6 and \
                                      abs(value_factor - 1.0) < 1e-6)

        if not needs_color_processing:
            # 如果没有颜色调整参数，函数行为类似于文件复制
            print(f"  所有HSV调整参数均为默认值。SVG颜色未作修改，直接输出到: {output_svg_path}")
            tree.write(output_svg_path, encoding="utf-8", xml_declaration=True)
            return

        # 遍历SVG树中的所有元素
        for element in root.iter():
            # 跳过非元素节点 (如注释、处理指令等)
            if not isinstance(element.tag, str) or '}' not in element.tag:
                continue
            
            # 遍历元素上可能包含颜色定义的属性
            # 使用 list(element.attrib.keys()) 是为了能在迭代时安全地修改属性字典
            for attr_name in list(element.attrib.keys()):
                if attr_name in color_attributes_to_modify:
                    original_color_str = element.get(attr_name)
                    
                    # 解析颜色字符串获取RGB分量和颜色本身的alpha值
                    r_orig, g_orig, b_orig, alpha_from_color_str = _parse_color_string_to_rgba(original_color_str)

                    # 如果颜色无法解析，或者是特殊值 (none, transparent, currentColor, hsl)，则跳过
                    if r_orig is None or isinstance(r_orig, str): # _parse_color_string_to_rgba 对特殊值返回字符串
                        # print(f"    跳过属性 '{attr_name}' 的特殊颜色值: '{original_color_str}'")
                        continue

                    # 获取元素上独立的opacity属性值 (如 'fill-opacity', 'stroke-opacity')
                    opacity_attr_name = attr_name + "-opacity"
                    opacity_attr_value_str = element.get(opacity_attr_name)
                    
                    attr_specific_opacity = 1.0 # 默认为完全不透明
                    if opacity_attr_value_str is not None:
                        try:
                            attr_specific_opacity = float(opacity_attr_value_str)
                        except ValueError:
                            # print(f"    警告: 无效的opacity值 '{opacity_attr_value_str}' 在属性 '{opacity_attr_name}'上。")
                            pass # 保持为1.0

                    # 计算最终要保留的有效原始透明度
                    # 这是颜色本身的alpha值与独立opacity属性值的乘积
                    effective_original_alpha = alpha_from_color_str * attr_specific_opacity
                    effective_original_alpha = max(0.0, min(1.0, effective_original_alpha)) #确保在0-1范围

                    # --- 在RGB颜色上进行HSV调整 ---
                    h_orig, s_orig, v_orig = _rgb_to_hsv(r_orig, g_orig, b_orig)

                    h_new = (h_orig + hue_rotate_degrees) % 360.0 # 色相循环
                    s_new = max(0.0, min(1.0, s_orig * saturation_factor)) # 饱和度限制在0-1
                    v_new = max(0.0, min(1.0, v_orig * value_factor))   # 明度限制在0-1

                    new_r, new_g, new_b = _hsv_to_rgb(h_new, s_new, v_new)
                    # --- HSV调整完成 ---

                    # 将调整后的颜色设置为纯色十六进制码 (不含alpha)
                    new_color_hex = f"#{int(round(new_r)):02x}{int(round(new_g)):02x}{int(round(new_b)):02x}"
                    element.set(attr_name, new_color_hex)

                    # 根据计算出的 effective_original_alpha 更新或移除对应的opacity属性
                    if abs(effective_original_alpha - 1.0) < 1e-6:  # 如果结果接近完全不透明
                        # 如果存在独立的opacity属性，则移除它，因为颜色已是不透明的
                        if opacity_attr_name in element.attrib:
                            del element.attrib[opacity_attr_name]
                    else:  # 如果结果是半透明的
                        # 设置或更新独立的opacity属性
                        element.set(opacity_attr_name, str(round(effective_original_alpha, 3))) # 保留3位小数精度

        # 写入修改后的SVG文件
        tree.write(output_svg_path, encoding="utf-8", xml_declaration=True)
        print(f"  ✅ SVG颜色属性直接修改完成: {output_svg_path}")

    except ET.ParseError as e:
        print(f"  😭 解析SVG文件 '{input_svg_path}' 出错: {e}")
    except Exception as e:
        print(f"  😭 处理SVG '{input_svg_path}' 时发生未知错误: {e}")


# --- 主执行逻辑 ---
if __name__ == '__main__':
    source_icon_dir = r"T:\d_maya\z_bs\icon\source"  # 您的原始SVG图标目录
    output_icon_dir = r"T:\d_maya\z_bs\icon"      # 您的最终输出目录

    # 为修复后的、作为基础版本的SVG创建一个临时子目录
    # 这样做可以保持主输出目录的整洁，这些是中间文件
    temp_repaired_bases_dir = os.path.join(output_icon_dir, "temp_repaired_bases")
    
    # 确保主输出目录和临时修复目录存在
    if not os.path.exists(output_icon_dir):
        os.makedirs(output_icon_dir)
        print(f"创建主输出目录: {output_icon_dir}")
    if not os.path.exists(temp_repaired_bases_dir):
        os.makedirs(temp_repaired_bases_dir)
        print(f"创建临时修复目录: {temp_repaired_bases_dir}")

    svg_file_list = find_all_svg_files(source_icon_dir)

    if not svg_file_list:
        print(f"在目录 '{source_icon_dir}' 中没有找到SVG文件。程序将退出。")
    else:
        print(f"总共找到 {len(svg_file_list)} 个SVG文件，开始批量处理...")

    for original_svg_path in svg_file_list:
        try:
            svg_file_basename = os.path.basename(original_svg_path)
            name, ext = os.path.splitext(svg_file_basename) # ext 会包含 '.' 例如 '.svg'

            print(f"\n--- 正在处理原始文件: {svg_file_basename} ---")

            # --- 步骤 1: (推荐) 修复原始SVG，创建干净的基础版本 ---
            # 这个修复后的版本将作为后续颜色调整的输入，以确保样式的统一和明确。
            repaired_base_file_path = os.path.join(temp_repaired_bases_dir, f"{name}_base_repaired{ext}")
            # print(f"  1. 修复原始SVG -> {repaired_base_file_path}") # repair_svg_for_qt内部已有打印
            repair_svg_for_qt(
                input_svg_path=original_svg_path,
                output_svg_path=repaired_base_file_path
            )
            
            # 定义后续颜色调整函数使用的输入路径 (即修复后的文件)
            input_path_for_color_modification = repaired_base_file_path

            # --- 步骤 2: 基于修复后的SVG，使用直接修改颜色属性的方法生成不同状态的变体 ---

            # 生成 Hover 变体 (提亮)
            hover_output_path = os.path.join(output_icon_dir, f"{name}_hover{ext}")
            # print(f"  2. 生成 Hover 变体 (直接改色) -> {hover_output_path}") # set_svg_colors_directly_hsv内部已有打印
            set_svg_colors_directly_hsv(
                input_svg_path=input_path_for_color_modification,
                output_svg_path=hover_output_path,
                value_factor=1.5  # 亮度增加50%
            )

            # 生成 Pressed 变体 (变暗且降低饱和度)
            pressed_output_path = os.path.join(output_icon_dir, f"{name}_pressed{ext}")
            # print(f"  3. 生成 Pressed 变体 (直接改色) -> {pressed_output_path}")
            set_svg_colors_directly_hsv(
                input_svg_path=input_path_for_color_modification,
                output_svg_path=pressed_output_path,
                saturation_factor=0.3,  # 饱和度调整为30%
                value_factor=0.7        # 明度/亮度调整为70%
            )

            # 生成 Normal (正常状态) 变体
            # 使用默认的HSV调整参数 (hue=0.0, saturation=1.0, value=1.0)
            # set_svg_colors_directly_hsv 函数内部会判断此时颜色不需调整，效果上是复制修复后的文件。
            normal_output_path = os.path.join(output_icon_dir, f"{name}{ext}")
            # print(f"  4. 生成 Normal 变体 (直接改色，无调整) -> {normal_output_path}")
            set_svg_colors_directly_hsv(
                input_svg_path=input_path_for_color_modification,
                output_svg_path=normal_output_path
            )
            # （或者，如果你确定修复后的版本就是最终的normal状态，也可以直接复制文件，避免一次解析和写入：
            # import shutil
            # shutil.copyfile(input_path_for_color_modification, normal_output_path)
            # print(f"  4. 复制修复后的基础版作为 Normal 状态 -> {normal_output_path}")
            # ）

            print(f"--- 完成SVG变体生成: {svg_file_basename} ---")

        except Exception as e: # 捕获处理单个文件时可能发生的任何异常
            print(f"😭 处理文件 '{original_svg_path}' 过程中发生严重错误: {e}")
            print("    将继续处理下一个文件...")
            # 根据需要，这里可以加入更详细的错误记录，或选择中断整个批处理
            
    print("\n🎉🎉🎉 所有SVG图标变体已按新流程生成完毕! 🎉🎉🎉")
    print(f"最终输出文件位于: {output_icon_dir}")
    print(f"修复后的中间基础文件位于 (可按需清理): {temp_repaired_bases_dir}")