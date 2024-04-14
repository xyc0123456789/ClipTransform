# -*- coding: utf-8 -*-
import re
import threading

import numpy as np
import win32clipboard
import time
import tkinter as tk
import urllib.parse

chatset = "gbk"


def do_nothing(data: str):
    return data


def strip_linebreaks(data: str):
    newdata = re.sub(r'-[\n\r]+', '', data)
    newdata = re.sub("[\n\r]+", " ", newdata)
    return newdata


def deduplication(data: str):
    newLines = data.split("\n")
    newL = []
    for i in newLines:
        if i is not None and len(i.strip()) > 3 and i.strip() not in newL:
            newL.append(i.strip())
    return "\n".join(newL)


ans = {}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def url_decode(data: str):
    try:
        decoded_data = urllib.parse.unquote(data)
        return url_decode(decoded_data)
    except Exception as e:
        return data



class ClipboardModifierApp:
    def __init__(self, funcList=None):
        if funcList is None:
            funcList = ["do_nothing", "strip_linebreaks", "url_decode", "deduplication"]
        self.last_clipboard_data = None
        self.selected_function = None
        self.lastFunc = None
        self.is_running = True
        root = tk.Tk()
        root.geometry("500x250")
        self.root = root
        self.root.title("Clipboard Modifier")

        self.label = tk.Label(root, text="Select Function:")
        self.label.grid(row=0, column=0)

        self.functions = funcList
        self.function_var = tk.StringVar()
        self.function_var.set("do_nothing")
        self.function_dropdown = tk.OptionMenu(root, self.function_var, *self.functions)
        self.function_dropdown.grid(row=0, column=1)

        # Input field to display the original content
        self.original_content_label = tk.Label(root, text="Original Content:")
        self.original_content_label.grid(row=1, column=0)
        self.original_content_text = tk.Text(root, height=5, width=40)
        self.original_content_text.grid(row=1, column=1)

        # Input field to display the modified content
        self.modified_content_label = tk.Label(root, text="Modified Content:")
        self.modified_content_label.grid(row=2, column=0)
        self.modified_content_text = tk.Text(root, height=5, width=40, state="disabled")
        self.modified_content_text.grid(row=2, column=1)

        self.processing_thread = threading.Thread(target=self.process_option)
        self.processing_thread.start()
        self.clipboard_monitor_thread = threading.Thread(target=self.clipboard_monitor)
        self.clipboard_monitor_thread.start()

    def on_closing(self):
        if self.is_running:
            self.is_running = False
            self.root.destroy()

    def process_option(self):
        while self.is_running:
            self.selected_function = self.function_var.get()
            if self.lastFunc != self.selected_function:
                self.lastFunc = self.selected_function
                self.doOnce(replace=True)
            time.sleep(0.5)  # 1秒的处理间隔

    def clipboard_monitor(self):
        self.last_clipboard_data = None
        while self.is_running:
            self.doOnce()
            # 设置适当的时间间隔来减少循环的频率
            time.sleep(1)  # 1秒的检测间隔

    def doOnce(self, replace=False):
        # 打开剪贴板
        win32clipboard.OpenClipboard(0)
        try:
            # 获取剪贴板内容
            clipboard_data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
            new_clipboard_data = clipboard_data.decode(chatset)
            # 检查是否发生了变化
            if new_clipboard_data != self.last_clipboard_data or replace:

                self.original_content_text.config(state="normal")
                self.modified_content_text.config(state="normal")

                self.original_content_text.delete(1.0, "end")
                self.original_content_text.insert("end", new_clipboard_data)

                if self.selected_function is None or self.selected_function == "":
                    self.last_clipboard_data = new_clipboard_data
                else:
                    self.last_clipboard_data = eval(self.selected_function)(new_clipboard_data)

                    # 将修改后的内容写入剪贴板
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardData(win32clipboard.CF_TEXT, self.last_clipboard_data.encode(chatset))
                self.modified_content_text.delete(1.0, "end")
                self.modified_content_text.insert("end", self.last_clipboard_data)
                # print(new_clipboard_data, self.last_clipboard_data)
        except Exception as e:
            pass
        finally:
            # 关闭剪贴板
            try:
                win32clipboard.CloseClipboard()
            except Exception:
                pass


if __name__ == "__main__":
    app = ClipboardModifierApp()
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    try:
        app.root.mainloop()
    except KeyboardInterrupt:
        app.on_closing()
    finally:
        app.on_closing()

    # pip install pyinstaller
    # pyinstaller --onefile --noconsole util_package/clipboardUtil.py
