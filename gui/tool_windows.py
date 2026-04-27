import tkinter as tk
from tkinter import ttk, messagebox
from tools.port_scanner import PortScanner
import threading
import time

class PortScannerWindow:
    def __init__(self, parent):
        self.parent = parent
        self.scanner = PortScanner()
        self.scan_thread = None
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标题
        ttk.Label(self.main_frame, text="端口扫描器", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # 创建输入区域
        input_frame = ttk.LabelFrame(self.main_frame, text="扫描设置")
        input_frame.pack(fill=tk.X, pady=10)
        
        # 目标IP/域名
        ttk.Label(input_frame, text="目标IP/域名:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.target_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.target_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        # 端口范围
        ttk.Label(input_frame, text="端口范围:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.start_port_var = tk.StringVar(value="1")
        ttk.Entry(input_frame, textvariable=self.start_port_var, width=10).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(input_frame, text="-").grid(row=1, column=1, padx=110, pady=5, sticky=tk.W)
        self.end_port_var = tk.StringVar(value="1024")
        ttk.Entry(input_frame, textvariable=self.end_port_var, width=10).grid(row=1, column=1, padx=120, pady=5, sticky=tk.W)
        
        # 线程数
        ttk.Label(input_frame, text="线程数:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.threads_var = tk.StringVar(value="100")
        ttk.Entry(input_frame, textvariable=self.threads_var, width=10).grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        # 超时设置
        ttk.Label(input_frame, text="超时(秒):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.timeout_var = tk.StringVar(value="1")
        ttk.Entry(input_frame, textvariable=self.timeout_var, width=10).grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        # 创建控制按钮区域
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="开始扫描", command=self.start_scan)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="停止扫描", command=self.stop_scan, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="清除结果", command=self.clear_results)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 创建进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        # 创建结果区域
        result_frame = ttk.LabelFrame(self.main_frame, text="扫描结果")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 创建结果文本框
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
    def start_scan(self):
        # 获取输入值
        target = self.target_var.get().strip()
        start_port = self.start_port_var.get().strip()
        end_port = self.end_port_var.get().strip()
        threads = self.threads_var.get().strip()
        timeout = self.timeout_var.get().strip()
        
        # 验证输入
        if not target:
            messagebox.showerror("错误", "请输入目标IP或域名")
            return
        
        try:
            start_port = int(start_port)
            end_port = int(end_port)
            threads = int(threads)
            timeout = float(timeout)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return
        
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            messagebox.showerror("错误", "端口范围无效")
            return
        
        if threads < 1 or threads > 1000:
            messagebox.showerror("错误", "线程数应在1-1000之间")
            return
        
        # 清空结果
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"开始扫描目标: {target}\n")
        self.result_text.insert(tk.END, f"端口范围: {start_port}-{end_port}\n")
        self.result_text.insert(tk.END, f"线程数: {threads}\n")
        self.result_text.insert(tk.END, f"超时: {timeout}秒\n")
        self.result_text.insert(tk.END, f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 禁用按钮
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # 启动扫描线程
        self.scan_thread = threading.Thread(target=self.scan_thread_func, args=(target, start_port, end_port, threads, timeout))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        
        # 启动进度更新线程
        self.update_progress()
    
    def scan_thread_func(self, target, start_port, end_port, threads, timeout):
        try:
            open_ports = self.scanner.start_scan(target, start_port, end_port, threads, timeout)
            
            # 显示结果
            self.result_text.insert(tk.END, f"\n扫描完成!\n")
            self.result_text.insert(tk.END, f"结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.result_text.insert(tk.END, f"发现 {len(open_ports)} 个开放端口:\n")
            
            if open_ports:
                for port in sorted(open_ports):
                    self.result_text.insert(tk.END, f"  - 端口 {port}\n")
            else:
                self.result_text.insert(tk.END, "  - 未发现开放端口\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"\n扫描过程中发生错误: {str(e)}\n")
        finally:
            # 启用按钮
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.progress_var.set(100)
    
    def update_progress(self):
        if self.scanner.is_running():
            progress = self.scanner.get_progress()
            self.progress_var.set(progress)
            self.parent.after(100, self.update_progress)
    
    def stop_scan(self):
        self.scanner.stop_scan()
        self.result_text.insert(tk.END, "\n扫描已停止\n")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.progress_var.set(0)