import json
import time
import shutil
import os
from datetime import datetime

'''
谷歌浏览器bai书签并不是以文du件夹的方式保存，而zhi是保存在一个Bookmarks文件dao中。查看该文件
位置方法：
1.打开谷歌浏览器，在地址栏中输入chrome://version/ 按回车键打开。
2.这时可以看到具体的“个人资料路径”
'''


def timestamp_to_unix(timestamp):
    """
    将 Chrome 的时间戳（以微秒为单位，从 1601 年 1 月 1 日开始）转换为 Unix 时间戳（以秒为单位，从 1970 年 1 月 1 日开始）。
    """
    if timestamp == "0":
        return "0"
    # Chrome 时间戳基准为 1601-01-01，Unix 时间戳基准为 1970-01-01
    chrome_epoch_start = datetime(1601, 1, 1)
    unix_epoch_start = datetime(1970, 1, 1)
    epoch_difference = (unix_epoch_start - chrome_epoch_start).total_seconds()
    # 将 Chrome 时间戳转换为秒
    return str(int(int(timestamp) / 1000000 - epoch_difference))


def parse_bookmarks(json_data, indent=0):
    """
    递归解析书签目录和书签列表，生成 HTML 格式字符串。
    """
    html = []
    indent_space = " " * (indent * 4)  # 每级目录缩进 4 空格

    # 判断当前书签节点是否有子目录或书签
    if json_data.get("type") == "folder":
        # 如果是文件夹，生成文件夹的 HTML 结构
        name = json_data["name"]
        date_added = timestamp_to_unix(json_data.get("date_added", "0"))
        date_modified = timestamp_to_unix(json_data.get("date_modified", "0"))
        html.append(f'{indent_space}<DT><H3 ADD_DATE="{date_added}" LAST_MODIFIED="{date_modified}">{name}</H3>')
        html.append(f'{indent_space}<DL><p>')
        for child in json_data.get("children", []):
            html.append(parse_bookmarks(child, indent + 1))
        html.append(f'{indent_space}</DL><p>')
    elif json_data.get("type") == "url":
        # 如果是书签，生成书签的 HTML 结构
        url = json_data["url"]
        name = json_data["name"]
        date_added = timestamp_to_unix(json_data.get("date_added", "0"))
        html.append(f'{indent_space}<DT><A HREF="{url}" ADD_DATE="{date_added}">{name}</A>')

    return "\n".join(html)


def convert_bookmarks_bak_to_html(input_file, output_file):
    """
    将 Chrome 的 bookmarks.bak 文件（JSON 格式）转换为 HTML 格式。
    """
    # 读取 JSON 文件
    with open(input_file, "r", encoding="utf-8") as f:
        bookmarks_data = json.load(f)

    # 获取书签的根目录（一般是 "roots" 节点）
    roots = bookmarks_data.get("roots", {})
    html_content = []

    # 添加 HTML 的头部信息（符合 Chrome 导出格式）
    html_content.append('<!DOCTYPE NETSCAPE-Bookmark-file-1>')
    html_content.append('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">')
    html_content.append('<TITLE>Bookmarks</TITLE>')
    html_content.append('<H1>Bookmarks</H1>')
    html_content.append('<DL><p>')

    # 遍历根目录中的每个节点（如书签栏、其他书签等）
    for key, root in roots.items():
        if isinstance(root, dict) and "children" in root:
            html_content.append(parse_bookmarks(root))

    html_content.append('</DL><p>')

    # 写入 HTML 文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))

    print(f"成功将书签文件从 JSON 转换为 HTML：{output_file}")


if __name__ == "__main__":
    # 源文件路径（要复制的文件）
    source_file = r'C:\Users\OMEN\AppData\Local\Google\Chrome\User Data\Default\Bookmarks.bak'

    # 获取当前目录作为目标路径
    destination_dir = './'

    # 获取源文件的文件名和扩展名
    file_name, file_extension = os.path.splitext(os.path.basename(source_file))

    # 获取当前时间戳（格式为：YYYYMMDD_HHMMSS）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # 构造目标文件名（在文件名后添加时间戳）
    new_file_name = f"{file_name}_{timestamp}{file_extension}"

    # 构造目标文件的完整路径
    destination_file = f"./output/{os.path.join(destination_dir, new_file_name)}"

    # 复制文件并重命名
    shutil.copy(source_file, destination_file)

    print(f"文件已复制并重命名为：{destination_file}")
    # ------这里用于调用转换函数----------
    # 输入文件（bookmarks.bak 的路径）
    input_file = destination_file

    # 输出文件（生成的 bookmarks.html 的路径）
    output_file = f"./output/{file_name}_{timestamp}.html"

    # 调用转换函数
    convert_bookmarks_bak_to_html(input_file, output_file)
