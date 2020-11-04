from tkinter import Tk
from tkinter import Menu
from tkinter import StringVar
from tkinter import Spinbox
from tkinter import ttk
from tkinter import LabelFrame
import tkinter.font as tkFont
import tkinter.messagebox 

import wmi 

class AppUI():
    m_branchs = ['分行本部','柯桥支行','嵊州支行','上虞支行','世纪街支行','诸暨支行','新昌支行']
    m_ips = ['','11.43.1.','11.43.2.','11.43.3.','11.43.4.','11.43.5.','11.43.6.']
    m_floorIPs = ['11.43.128.','11.43.129.','11.43.130.','11.43.131.','11.43.132.','11.43.133.','11.43.134.']
    m_floors = ['一楼','二楼','三楼','四楼','五楼','六楼','十八楼']

    def __init__(self):
        self.root = Tk()
        self.root.option_add('*Dialog.msg.font', 'Helvetica 12')
        self.ft = tkFont.Font(family='FangSong',size=20, weight=tkFont.BOLD)   
        
        self.selectedBranch = ''
        self.selectedFloor = ''

        self.create_menu(self.root)
        self.create_content(self.root)
        self.root.title("绍兴分行运维自动化工具")
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
        frm = LabelFrame(height = 200,width = 300,text = 'IP管理',borderwidth=3)
        frm.grid(row=0,column=0,pady=10)
                 
        ttk.Label(frm,text=" 机 构: ",font=self.ft).grid(row=0,column=0,pady=10)
        self.branchWidget = ttk.Combobox(frm,textvariable=StringVar,state="readonly",width=10,font=self.ft) 
        self.branchWidget['values'] = self.m_branchs
        self.branchWidget.bind("<<ComboboxSelected>>", self.branchGet)
        self.branchWidget.grid(row=0,column=1,columnspan=3,padx=10,pady=10)
        
        
        ttk.Label(frm,text=" 楼 层: ",font=self.ft).grid(row=1,column=0,pady=10)
        self.floorWidget = ttk.Combobox(frm,textvariable=StringVar,state="disabled",width=10,font=self.ft)
        
        self.floorWidget.bind("<<ComboboxSelected>>", self.floorGet)
        self.floorWidget.grid(row=1,column=1,columnspan=3,padx=10,pady=10)
        
        ttk.Label(frm,text=" 座位号: ",font=self.ft).grid(row=2,column=0,pady=10)
        ttk.Label(frm,text="  A",font=self.ft).grid(row=2,column=1,pady=10)
        self.netportWidget = Spinbox(frm,from_=0,to=255, width=5, bd=8,font=self.ft) 
        self.netportWidget.grid(row=2,column=2)
        button = ttk.Button(frm,text ="点我查看座位号", command = self.viewHelp)
        button.grid(row=2,column=3)
        
        
        ttk.Button(frm,text="设置IP",command=self.changeIP).grid(row=3,column=0,padx=10,pady=10)
        self.progress_bar=ttk.Progressbar(frm,orient='horizontal',mode='determinate',maximum=100,length=180)
        self.progress_bar.grid(row=3,column=1,columnspan=3,padx=10,pady=10)
    def viewHelp(self):
        tkinter.messagebox.showwarning('提示','请查座位下网口号上\n    A口后面的数字'+
                                                             '\n     Axx   Bxx'+ 
                                                             '\n      口      口')
        
    def branchGet(self,Event):
        self.selectedBranch=self.branchWidget.get()
        if self.m_branchs[0] == self.selectedBranch:
            self.floorWidget['values'] = self.m_floors
            self.floorWidget.configure(state='readonly')
        else:            
            self.floorWidget.set('')
            self.floorWidget.configure(state='disabled')
        
    def floorGet(self,Event):
        self.selectedFloor=self.floorWidget.get()
        
    def getArrIndex(self,ele,array):
        for i in range(len(array)):
            if ele==array[i]:
                return i
        
        return -1
    
    def updateProcess(self,process):
        self.progress_bar['value']=process
        self.progress_bar.update()

    def changeIP(self):
            
        ip = ''
        subnetmask = '255.255.255.0'
        gateway = '' 
        
        self.updateProcess(10)
        
        selectedBranch = self.getArrIndex(self.selectedBranch,self.m_branchs)
        if -1 == selectedBranch:
            self.updateProcess(0)
            tkinter.messagebox.showwarning('提示','请选择机构')
            return
        elif 0 == selectedBranch:#分行本级
            selectedFloor = self.getArrIndex(self.selectedFloor,self.m_floors)
            if -1 == selectedFloor:
                self.updateProcess(0)
                tkinter.messagebox.showwarning('提示','请选择楼层')
                return
            ip = self.m_floorIPs[selectedFloor]
        else:
            ip = self.m_ips[selectedBranch]
            
        self.updateProcess(30)            
            
        netport = self.netportWidget.get()    
        if '0' == netport:
            self.updateProcess(0)
            tkinter.messagebox.showwarning('提示','请选择座位号')
            return
        gateway = ip + '254'
        ip = ip + netport
        dns = ['11.43.240.193','11.43.240.194']
        
        print('ip:' + ip + ',gateway:' + gateway)
        
        self.updateProcess(40)

        # Obtain network adaptors configurations
        nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
        # First network adaptor
        nic = nic_configs[0]
        
        self.updateProcess(60)
         
         
        # Set IP address, subnetmask and default gateway
        # Note: EnableStatic() and SetGateways() methods require *lists* of values to be passed
        returnValue = nic.EnableStatic(IPAddress=[ip],SubnetMask=[subnetmask])
        self.updateProcess(80)
        nic.SetDNSServerSearchOrder(DNSServerSearchOrder=dns)
        nic.SetGateways(DefaultIPGateway=[gateway])
        
        self.updateProcess(100)
        
        if 0 == returnValue[0]:
            tkinter.messagebox.showwarning('提示','ip修改成功！')
        else:
            tkinter.messagebox.showerror('错误','ip修改失败！')
        
        self.updateProcess(0)


if __name__ == "__main__":
    myapp = AppUI()