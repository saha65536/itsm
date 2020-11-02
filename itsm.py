from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import tkinter.filedialog as dir
import tkinter
import tkinter.messagebox 

import time

class AppUI():

    def __init__(self):
        self.root = Tk()
        self.ft = tkFont.Font(size=20, weight=tkFont.BOLD)
        self.progress_bar=ttk.Progressbar(orient='horizontal',mode='determinate',maximum=100,length=180)
        s = ttk.Style()
        
        s.configure('my.TButton', font=('隶书', 20))
        self.create_menu(self.root)
        self.create_content(self.root)
        self.root.title("运维自动化工具")
        self.root.update()
        
        self.center_window()
        
    
    def center_window(self):  
        curWidth = self.root.winfo_width()  # get current width
        curHeight = self.root.winfo_height()  # get current height
        scnWidth, scnHeight = self.root.maxsize()  # get screen width and height
        tmpcnf = '+%d+%d' % ((scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
        self.root.geometry(tmpcnf)
        self.root.mainloop()

    def create_menu(self,root):
        #创建菜单栏
        menu = Menu(root)

        #创建二级菜单
        help_menu = Menu(menu,tearoff=0)
        help_menu.add_command(label="本系统由宁波银行绍兴分行金融科技部开发。"+
                              "\r\n如有问题请联系运维阮金国 王立刚8831")


        about_menu = Menu(menu,tearoff=0)
        about_menu.add_command(label="version:1.0")

        #在菜单栏中添加以下一级菜单
        menu.add_cascade(label="帮助",menu=help_menu)
        menu.add_cascade(label="关于",menu=about_menu)
        root['menu'] = menu

    def create_content(self, root):
                 
        ttk.Label(text=" 机 构: ",font=self.ft).grid(row=0,column=0,pady=10)
        spinBranch = Spinbox(width=10, bd=8,font=self.ft) 
        spinBranch['values'] = ('分行营业部','柯桥支行')
        spinBranch.grid(row=0,column=1,padx=10,pady=10)
        
        
        ttk.Label(text=" 楼 层: ",font=self.ft).grid(row=1,column=0,pady=10)
        floorWidget = ttk.Combobox(textvariable=StringVar,state="readonly",width=20)
        floorWidget['values'] = ('一楼','二楼','三楼')
        floorWidget.grid(row=1,column=1,padx=10,pady=10)
        
        ttk.Label(text=" 座位号: ",font=self.ft).grid(row=2,column=0,pady=10)
        spin = Spinbox(from_=0,to=255, width=5, bd=8,font=self.ft) 
        spin.grid(row=2,column=1)
        
        
        ttk.Button(text="设置IP",command=self.changeIP).grid(row=3,column=0,padx=10,pady=10)
        
        self.progress_bar.grid(row=3,column=1,padx=10,pady=10)


    def changeIP(self):
        for i in range(101):
            self.progress_bar['value']=i
            #progressbarVar.set(i)
            self.progress_bar.update()
            time.sleep(0.05)
        
        tkinter.messagebox.showinfo('提示','设置IP成功！')



if __name__ == "__main__":
    AppUI()