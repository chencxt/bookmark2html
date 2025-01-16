hello!
这是一个基于python的谷歌书签转换为可以被导入的HTML的脚本。
你可以调试“autoBackup.txt”，来实现自动化备份书签
“autoBackup.txt”内容解析：
	F: //跳转到代码所在盘符
	cd F:\CodeWorkspace\Python\bookmark2html //跳转到代码所在路径
	python main.py //执行代码
	git add output/ //往下都是将新内容push到github的内容
	git commit -m "auto output test"
	git push 
调整完成后，将“autoBackup.txt”重命名为“autoBackup.bat”，然后放在开机自启动文件夹内，就可以实现自动化开机备份书签并同步到github的远程仓库中。
