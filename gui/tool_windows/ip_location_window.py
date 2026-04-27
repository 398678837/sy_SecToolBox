import tkinter as tk
from tkinter import ttk, messagebox
from tools.ip_location import IPLocation
import threading
import time

class IPLocationWindow:
    def __init__(self, parent):
        self.parent = parent
        self.ip_locator = IPLocation()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标题
        ttk.Label(self.main_frame, text="IP归属地查询", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # 创建输入区域
        input_frame = ttk.LabelFrame(self.main_frame, text="查询设置")
        input_frame.pack(fill=tk.X, pady=10)
        
        # 单个IP查询
        ttk.Label(input_frame, text="单个IP地址:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.single_ip_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.single_ip_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        # 批量IP查询
        ttk.Label(input_frame, text="批量IP地址:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.batch_ip_var = tk.Text(input_frame, width=30, height=5)
        self.batch_ip_var.grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(input_frame, text="（每行一个IP）").grid(row=2, column=1, padx=10, pady=2, sticky=tk.W)
        
        # 创建控制按钮区域
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.single_query_btn = ttk.Button(button_frame, text="查询单个IP", command=self.query_single_ip)
        self.single_query_btn.pack(side=tk.LEFT, padx=5)
        
        self.batch_query_btn = ttk.Button(button_frame, text="批量查询", command=self.query_batch_ip)
        self.batch_query_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="清除结果", command=self.clear_results)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 创建结果区域
        result_frame = ttk.LabelFrame(self.main_frame, text="查询结果")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建结果文本框
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=15)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
    def query_single_ip(self):
        ip = self.single_ip_var.get().strip()
        if not ip:
            messagebox.showerror("错误", "请输入IP地址")
            return
        
        # 清空结果
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"正在查询 IP: {ip}\n\n")
        
        # 执行查询
        result = self.ip_locator.get_location(ip)
        
        # 显示结果
        if "error" in result:
            self.result_text.insert(tk.END, f"查询失败: {result['error']}\n")
        else:
            self.result_text.insert(tk.END, f"IP地址: {result.get('ip')}\n")
            self.result_text.insert(tk.END, f"国家: {result.get('country')}\n")
            self.result_text.insert(tk.END, f"地区: {result.get('region')}\n")
            self.result_text.insert(tk.END, f"城市: {result.get('city')}\n")
            self.result_text.insert(tk.END, f"ISP: {result.get('isp')}\n")
            self.result_text.insert(tk.END, f"组织: {result.get('org')}\n")
            self.result_text.insert(tk.END, f"AS: {result.get('as')}\n")
            self.result_text.insert(tk.END, f"纬度: {result.get('latitude')}\n")
            self.result_text.insert(tk.END, f"经度: {result.get('longitude')}\n")
            self.result_text.insert(tk.END, f"时区: {result.get('timezone')}\n")
    
    def query_batch_ip(self):
        ip_text = self.batch_ip_var.get(1.0, tk.END).strip()
        if not ip_text:
            messagebox.showerror("错误", "请输入IP地址列表")
            return
        
        ip_list = [ip.strip() for ip in ip_text.split('\n') if ip.strip()]
        if not ip_list:
            messagebox.showerror("错误", "请输入有效的IP地址列表")
            return
        
        # 清空结果
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"正在批量查询 {len(ip_list)} 个IP地址\n\n")
        
        # 执行批量查询
        results = self.ip_locator.batch_query(ip_list)
        
        # 显示结果
        for i, result in enumerate(results):
            self.result_text.insert(tk.END, f"=== IP {i+1} ===\n")
            if "error" in result:
                self.result_text.insert(tk.END, f"查询失败: {result['error']}\n")
            else:
                self.result_text.insert(tk.END, f"IP地址: {result.get('ip')}\n")
                self.result_text.insert(tk.END, f"国家: {result.get('country')}\n")
                self.result_text.insert(tk.END, f"地区: {result.get('region')}\n")
                self.result_text.insert(tk.END, f"城市: {result.get('city')}\n")
                self.result_text.insert(tk.END, f"ISP: {result.get('isp')}\n")
            self.result_text.insert(tk.END, "\n")
    
    def clear_results(self):
        self.result_text.delete(1.0, tk.END)