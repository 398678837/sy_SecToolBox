# sy_SecToolBox 安全工具箱

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

sy_SecToolBox 是一个基于 Python + Tkinter 开发的 Windows 可视化安全工具集合，旨在为个人学习网络安全提供实用工具。项目采用轻量化设计，专注于本地和授权测试环境的安全检测与分析，严格遵循合法合规原则，仅用于技术学习研究目的。

## 技术栈

- **开发语言**：Python 3.8+
- **GUI框架**：Tkinter（内置库，无需额外安装）
- **打包工具**：PyInstaller（将项目打包为独立可执行文件）
- **网络库**：socket（内置库，用于网络相关功能）

## 功能列表

### 已实现功能
- **多线程端口扫描器**：支持单个IP、IP范围、域名扫描，可自定义端口范围和扫描线程数

### 计划实现功能
1. **IP归属地查询**
2. **密码强度检测**
3. **随机安全密码生成器**
4. **文件Hash校验工具**
5. **时间戳/日期互转**
6. **Base64加解密**
7. **URL编解码工具**
8. **DNS解析查询**
9. **局域网存活主机探测**
10. **子域名简易枚举**
11. **简易HTTP模拟请求工具**
12. **本地端口进程监控**
13. **网络延迟测速工具**
14. **批量文本加密解密**
15. **特殊字符过滤检测**
16. **ARP缓存查看**
17. **简易日志关键词分析**
18. **CVE漏洞快速查询**
19. **简易端口转发工具**
20. **全局UI统一美化**
21. **深色/浅色双主题切换**

## 安装说明

### 方法一：直接运行源码
1. 确保已安装 Python 3.8 或更高版本
2. 克隆或下载本项目到本地
3. 进入项目目录
4. 运行 `python main.py` 启动应用

### 方法二：使用打包后的可执行文件
（后续版本会提供）

## 使用方法

1. 启动应用后，从左侧导航栏选择需要使用的工具
2. 填写相关参数，点击「开始」按钮执行操作
3. 查看结果区域的输出信息
4. 可使用「清除结果」按钮清空结果，「导出结果」按钮保存结果（后续版本支持）

## 项目结构

```
sy_SecToolBox/
├── main.py              # 主程序入口
├── tools/              # 工具模块目录
│   ├── __init__.py
│   └── port_scanner.py  # 端口扫描器
├── gui/                # GUI界面模块
│   ├── __init__.py
│   ├── main_window.py  # 主窗口
│   └── tool_windows.py  # 工具子窗口
├── utils/              # 工具函数
│   └── __init__.py
├── data/               # 数据目录
│   └── cve_database/    # CVE漏洞数据库
├── docs/               # 文档目录
│   ├── development_plan.md  # 开发规划文档
│   └── developer_log.md     # 开发者日志
├── requirements.txt    # 依赖文件
└── README.md           # 项目说明
```

## 开发计划

项目采用12期迭代开发计划，每期实现2个功能，循序渐进、由浅入深，节奏平缓适合长期开发学习。详细开发计划请参考 [开发规划文档](docs/development_plan.md)。

## 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 注意事项

- **合法性**：本工具仅用于授权测试环境，严格遵守法律法规
- **安全性**：确保在使用本工具时采取必要的安全措施
- **责任**：使用本工具产生的一切后果由使用者自行承担

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

## 联系方式

- 项目地址：[GitHub](https://github.com/yourusername/sy_SecToolBox)
- 问题反馈：[Issues](https://github.com/yourusername/sy_SecToolBox/issues)

---

**免责声明**：本工具仅供学习和研究使用，请勿用于任何非法用途。