# 剪贴板内容转换

Windows 复制内容后调用指定方法来修改剪贴板中的内容，目前仅限文本

## 现有实现

- do_nothing：不进行任何修改
- strip_linebreaks：删除换行符，主要用于复制英文文献的场景
- url_decode：对复制的url进行递归解码
- deduplication：对重复行去重



## 使用方法

```shell
python main.py
```

或者使用pyinstaller 打包成exe来使用

```shell
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
```



## 可能的问题

1、 **ImportError: DLL load failed while importing win32clipboard: 找不到指定的模块。**

**解决方法：**重新安装pywin32





## 未来改进

- [ ] 更多使用场景实现，如增加本地键值对存储，填写页面表单
- [ ] 将具体实现分类放置至一个文件夹
- [ ] 使用llm自动判断使用场景来调用对应方法



