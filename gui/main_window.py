import tkinter as tk
from tkinter import ttk
from gui.tool_windows import PortScannerWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("sy_SecToolBox - 安全工具箱")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # 设置主题
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建左侧导航栏
        self.nav_frame = ttk.Frame(self.main_frame, width=200)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 创建导航栏标题
        ttk.Label(self.nav_frame, text="工具列表", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # 创建工具按钮
        self.tool_buttons = []
        
        # 网络工具
        ttk.Label(self.nav_frame, text="网络工具", font=('Arial', 10, 'bold'), foreground='#1a237e').pack(anchor=tk.W, pady=(10, 5))
        self.port_scan_btn = ttk.Button(self.nav_frame, text="端口扫描器", width=20, command=self.open_port_scanner)
        self.port_scan_btn.pack(pady=2)
        
        # 占位按钮，后续会添加其他工具
        ttk.Button(self.nav_frame, text="IP归属地查询", width=20, state=tk.DISABLED).pack(pady=2)
        ttk.Button(self.nav_frame, text="DNS解析查询", width=20, state=tk.DISABLED).pack(pady=2)
        ttk.Button(self.nav_frame, text="局域网存活主机探测", width=20, state=tk.DISABLED).pack(pady=2)
        
        # 安全工具
        ttk.Label(self.nav_frame, text="安全工具", font=('Arial', 10, 'bold'), foreground='#1a237e').pack(anchor=tk.W, pady=(10, 5))
        ttk.Button(self.nav_frame, text="密码强度检测", width=20, state=tk.DISABLED).pack(pady=2)
        ttk.Button(self.nav_frame, text="随机密码生成器", width=20, state=tk.DISABLED).pack(pady=2)
        ttk.Button(self.nav_frame, text="文件Hash校验", width=20, state=tk.DISABLED).pack(pady=2)
        
        # 创建右侧工作区
        self.work_frame = ttk.Frame(self.main_frame)
        self.work_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 创建工作区标题
        self.work_title = ttk.Label(self.work_frame, text="欢迎使用 sy_SecToolBox", font=('Arial', 14, 'bold'))
        self.work_title.pack(pady=20)
        
        self.work_desc = ttk.Label(self.work_frame, text="请从左侧选择一个工具开始使用", font=('Arial', 10))
        self.work_desc.pack()
        
        # 创建底部状态栏
        self.status_frame = ttk.Frame(self.root, height=20)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_frame, text="就绪", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.version_label = ttk.Label(self.status_frame, text="版本 1.0.0", anchor=tk.E)
        self.version_label.pack(side=tk.RIGHT, padx=10)
        
    def open_port_scanner(self):
        # 清空工作区
        for widget in self.work_frame.winfo_children():
            widget.destroy()
        
        # 创建端口扫描器窗口
        PortScannerWindow(self.work_frame)
        
        # 更新状态栏
        self.status_label.config(text="端口扫描器已打开")