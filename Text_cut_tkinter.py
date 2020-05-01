# -*- coding: utf-8 -*-
# 词调试文件：Text_cut_wdy.xlsx

import pandas as pd
import tkinter.messagebox
import winreg
import tkinter as tk
import win32ui
from os import chdir, path
from jieba.analyse import extract_tags
from re import sub, findall
from collections import Counter

cut_wr=None 
class txt():
    '''初始化属性
    word_cut切词，word_count词频，word_before_after词的前后几个字
    '''
    def __init__(self,filename):
        self.filename=filename

    def word_cut(self): #cut_w=[] # 存放数据
        cut_w=[];ct=0;cut_words=""
        Target=pd.read_excel(self.filename).fillna("A").iloc[:, -1] # 文本在最后一行
        for word in Target:
            ct+=1
            if ct%2000==0: print(ct) # 看速度
            word=sub("[\：\·\—\，\。\“ \”\>\）\【\】\？\！\,\/\ ]", "|", str(word).strip("\n").strip("\r\n"))
            cut_w.append(word)
            seg_list = extract_tags(word, topK=None)  # textrank
            cut_words += ("/".join(seg_list)+"/||")
        global cut_wr
        cut_wr = "||".join(cut_w) # 段落||隔开
        self.all_words = cut_words.split("/") # 词/隔开
        
    def word_count(self):
        self.word_cut() #!!!!!!!!!!!!记得引用
        cout = Counter(self.all_words) # # 用于统计词和词频
        wd = []; quent = [] # 词、频
        for (k, v) in cout.most_common():
            wd.append(k)
            quent.append(v)
        qieci = pd.DataFrame([wd, quent]).T
        qieci.to_excel("切词结果textrank.xlsx", encoding='GB18030')
    
    def word_before_after(self, wrd, m, n, L):
        sword = "("+"\S"*m+wrd+"\S"*n+")" # 前m个字，后n个字
        w = findall(sword,cut_wr)
        c2 = Counter(w)
        wd2 = []; quent2 = []
        for (k, v) in c2.most_common():
            if v > L:  # 出现L次之上
                wd2.append(k)
                quent2.append(v)
        pd.set_option('max_rows', 500)
        return pd.DataFrame([wd2, quent2]).T

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
desk=winreg.QueryValueEx(key, "Desktop")[0] # windows的桌面路径
chdir(desk)
dlg = win32ui.CreateFileDialog(1) # 1表示打开文件对话框
dlg.SetOFNInitialDir(desk)
dlg.DoModal()  # 设置打开文件对话框中的初始显示目录
filename = dlg.GetPathName()  # 获取选择的文件名称
mytxt=txt(filename) # 初始化

mytxt.word_count() # 切词输出
print("-----------------分析完成-----------------")

# ..................................窗口初始化.............................
# 大小、文本框、文本框说明
window = tk.Tk()
window.title('文本切词')  # 控件名
window.geometry('270x415')  # 窗口大小
# 交互式文本框
e1 = tk.Entry(window, show='', width=10)
e2 = tk.Entry(window, show='', width=5)
e3 = tk.Entry(window, show='', width=5)
e4 = tk.Entry(window, show='', width=5)
# 文本框的位置
e1.grid(row=1, column=1, sticky=tk.W)
e2.grid(row=2, column=1, sticky=tk.W)
e3.grid(row=3, column=1, sticky=tk.W)
e4.grid(row=4, column=1, sticky=tk.W)
# 框的标签
tk.Label(window, text=filename.split("\\")[-1], bg='lightblue').grid(row=0, column=1, sticky=tk.W)  
tk.Label(window, text="正在分析：").grid(row=0, column=0, sticky=tk.E)
tk.Label(window, text="词（不要复制粘贴）", bg='red').grid(row=1, column=0, sticky=tk.E)
tk.Label(window, text="前_个字：").grid(row=2, column=0, sticky=tk.E)
tk.Label(window, text="后_个字：").grid(row=3, column=0, sticky=tk.E)
tk.Label(window, text="出现_次以上").grid(row=4, column=0, sticky=tk.E)
tk.Label(window, text="结果：", bg='red').grid(row=6, column=0, sticky=tk.E)

# ..................................添加按钮 执行.............................
def insert_end():
    var1 = str(e1.get())
    var2 = int(e2.get())
    var3 = int(e3.get())
    var4 = int(e4.get())
    t.delete(1.0, tk.END)
    t.insert("end", mytxt.word_before_after(wrd=var1, m=var2, n=var3, L=var4), 'tag_1')
    t.insert("end", "\n查找完成")
b2 = tk.Button(window, text="执行", command=insert_end)  # 按钮，函数
b2.grid(row=5, column=1, sticky=tk.W)
t = tk.Text(window, height=18, width=25)
t.tag_config("tag_1", backgroun="yellow", foreground="red")
t.grid(row=6, column=1, sticky=tk.W)

# ..................................添加按钮 提示.............................
def hit_me():
    tk.messagebox.showinfo(
        title='提示', message='文本内容需要位于首个sheet，并且位于最后一列。最后的切词结果textrank.xlsx会出现在桌面')
tk.Button(window, text='提示', command=hit_me).grid(
    row=7, column=0, sticky=tk.E)  # 按钮，提示


window.mainloop()  # 动态
