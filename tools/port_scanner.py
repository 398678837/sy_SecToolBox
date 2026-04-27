import socket
import threading
import queue
import time
from datetime import datetime

class PortScanner:
    def __init__(self):
        self.open_ports = []
        self.scan_queue = queue.Queue()
        self.lock = threading.Lock()
        self.scan_running = False
        self.total_ports = 0
        self.scanned_ports = 0
        
    def scan_port(self, target, port, timeout=1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                    print(f"Port {port}: OPEN")
            sock.close()
        except Exception as e:
            pass
        finally:
            with self.lock:
                self.scanned_ports += 1
    
    def worker(self, target, timeout):
        while self.scan_running:
            try:
                port = self.scan_queue.get_nowait()
                self.scan_port(target, port, timeout)
                self.scan_queue.task_done()
            except queue.Empty:
                break
    
    def start_scan(self, target, start_port, end_port, threads=100, timeout=1):
        self.open_ports = []
        self.scanned_ports = 0
        self.total_ports = end_port - start_port + 1
        self.scan_running = True
        
        # 填充端口队列
        for port in range(start_port, end_port + 1):
            self.scan_queue.put(port)
        
        # 启动线程
        thread_list = []
        for i in range(threads):
            t = threading.Thread(target=self.worker, args=(target, timeout))
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        # 等待所有线程完成
        self.scan_queue.join()
        self.scan_running = False
        
        # 等待所有线程结束
        for t in thread_list:
            t.join()
        
        return self.open_ports
    
    def get_progress(self):
        if self.total_ports == 0:
            return 0
        return (self.scanned_ports / self.total_ports) * 100
    
    def stop_scan(self):
        self.scan_running = False
    
    def is_running(self):
        return self.scan_running