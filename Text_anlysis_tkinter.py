# -*- coding: utf-8 -*-
# 先Text_cut_wdy.xlsx，然后dict.xlsx

from pandas import DataFrame, read_excel, melt
from re import sub
from os import chdir, path
from win32ui import CreateFileDialog
import tkinter as tk
import tkinter.messagebox
import winreg


class txt2():
    '''初始化属性
    findkey匹配关键词，file_dict构造文本和字典，fenxi分析文本
    '''
    def __init__(self,filename,dictfile):
        self.filename=filename
        self.dictfile=dictfile
    
    def findkey(self,x,Keylist,MyDict): 
        find = ["其他问题"]
        for onekey in Keylist:
            for fkey in MyDict[onekey]:
                if fkey in x:
                    find.append(onekey)
        if len(find) > 1:
            find = find[1:]
        return list(set(find))

    def file_dict(self):
        # 构造词典
        df = read_excel(self.dictfile).fillna("A")
        MyDict = {col: df[col].tolist() for col in df.columns}
        for e in MyDict.keys():
            for li in range(len(MyDict[e])-1, -1, -1):
                if MyDict[e][li] == "A":
                    MyDict[e].remove("A")
        df["IID"] = range(0, len(df))
        df = melt(df, id_vars="IID")
        df["词频"] = 0
        df.drop(df[df["value"] == "A"].index, inplace=True)
        df = df.reset_index(drop=True)
        Keylist = MyDict.keys()
        # 构造文本
        Orign = read_excel(self.filename).fillna("A")  # 读取数据
        Target = DataFrame(Orign.iloc[:, -1]) 
        Target.columns = ["文本"]
        Target["ID"] = range(1, Target.shape[0]+1)
        for key in Keylist:
            Target[key] = 0
        Target["其他问题"] = 0
        return [MyDict,df,Target]
    
    def fenxi(self):
        source=self.file_dict()
        Stoplist = list(read_excel(self.dictfile, sheet_name="停用词")["停用词"])
        MyDict=source[1]; df=source[2]; Target=source[3]
        # 分析文本
        for i in Target["ID"]:
            if i%2000==0: print('第'+str(i)+'行')  # 查看进度
            word = Target["文本"][i-1]
            word = str(word).strip(" ").strip("\n").strip("\r\n")
            word = sub("[A-Za-z0-9\：\·\—\，\。\“ \”\>\）\【\】\？\！]", "/", word)
            wrd = str(word); k = 0
            for kv in list(df["value"]):
                k += 1
                if kv in wrd:
                    df.loc[k-1, "词频"] += 1
            for st in Stoplist:
                wrd = wrd.replace(st, "/")
            for wr in self.findkey(wrd,MyDict.keys(),MyDict):
                Target.loc[i-1, wr] = 1
        Target.to_excel("分析结果.xlsx", encoding='GB18030')
        df.to_excel("词频结果.xlsx", encoding='GB18030')


# .........................窗口控件.........................................
window = tk.Tk()
window.title('文本分析')
window.geometry('220x180')
tk.Label(window, text="分析的文本：").grid(row=0, column=0, sticky=tk.E)
tk.Label(window, text="词典文件：").grid(row=1, column=0, sticky=tk.E)
txt=None
# 获取桌面路径
def get_desktop():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]
# 选择文本文件和字典文件，并初始化类
def wenjian():
    desk = get_desktop()  # 桌面路径
    chdir(desk)
    dlg = CreateFileDialog(1)  # 1表示打开文件对话框
    dlg.SetOFNInitialDir(desk)  # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename = dlg.GetPathName()  # 获取选择的文件名称
    dlg.DoModal()
    dictfile = dlg.GetPathName() # 获取字典
    global txt
    txt = txt2(filename,dictfile)
    tk.Label(window, text=filename.split("\\")
         [-1], bg='lightblue').grid(row=0, column=1, sticky=tk.W)
    tk.Label(window, text=dictfile.split("\\")
         [-1], bg='lightblue').grid(row=1, column=1, sticky=tk.W)
# 执行分析 
def run():
    print("-----------------开始分析-----------------")
    txt.fenxi()
    tk.messagebox.showinfo(title='提示', message='分析完成')
    window.destroy()
# 提示
def hit_me():
    tk.messagebox.showinfo(
        title='再次提示', message='先选择文本文件，文本内容需要位于首个sheet，并且位于最后一列。然后 选择字典文件，用到的字典需要位于首个sheet(停用词sheet需要有)。分析结果.xlsx，词频结果.xlsx会出现在桌面')

b1 = tk.Button(window, text="选文本和词典", command=wenjian, background='lightgray')
b1.grid(row=2, column=1, sticky=tk.W)
b2 = tk.Button(window, text="开始分析", command=run, background='red')
b2.grid(row=3, column=1, sticky=tk.W)
tk.Button(window, text='提示', command=hit_me).grid(row=4, column=1, sticky=tk.W)

window.mainloop()
