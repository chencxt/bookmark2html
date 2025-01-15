
import shutil
import os
from datetime import datetime
'''
谷歌浏览器bai书签并不是以文du件夹的方式保存，而zhi是保存在一个Bookmarks文件dao中。查看该文件
位置方法：
1.打开谷歌浏览器，在地址栏中输入chrome://version/ 按回车键打开。
2.这时可以看到具体的“个人资料路径”
'''


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
destination_file = os.path.join(destination_dir, new_file_name)

# 复制文件并重命名
shutil.copy(source_file, destination_file)

print(f"文件已复制并重命名为：{destination_file}")


