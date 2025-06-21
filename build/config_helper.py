#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import json
import os
import sys
from pathlib import Path
import platform

# 设置Windows控制台编码并隐藏控制台窗口
if sys.platform == 'win32':
    import locale
    import ctypes
    try:
        # 隐藏控制台窗口
        if hasattr(sys, '_MEIPASS'):  # 只在打包后的exe中隐藏控制台
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
        # 尝试设置UTF-8编码
        os.system('chcp 65001 >nul 2>&1')
        # 设置默认编码
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

class ConfigHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("墨问MCP服务社区版 - 配置助手")
        self.root.geometry("700x600")
        
        # 获取可执行文件所在目录
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller打包环境
            if sys.platform == 'darwin':
                # macOS .app包的处理
                self.exe_dir = os.path.dirname(sys.executable)
                if '.app' in self.exe_dir:
                    # 从.app/Contents/MacOS回到.app同级目录
                    self.exe_dir = os.path.dirname(os.path.dirname(os.path.dirname(self.exe_dir)))
            else:
                self.exe_dir = os.path.dirname(sys.executable)
        else:
            # 开发环境
            self.exe_dir = os.path.dirname(os.path.abspath(__file__))
            
        # 自动检测平台
        system = platform.system().lower()
        if system == 'darwin':
            self.target_platform = 'macos'
        elif system == 'windows':
            self.target_platform = 'windows'
        else:
            self.target_platform = 'linux'
            
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主标题
        title_frame = tk.Frame(self.root, bg="#2E86AB", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="墨问MCP服务社区版 - 配置助手", 
                              font=("Arial", 16, "bold"),
                              bg="#2E86AB", fg="white")
        title_label.pack(expand=True)
        
        # 主内容
        main_frame = tk.Frame(self.root, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 平台特定说明
        platform_info = {
            'windows': "Windows版本配置助手",
            'macos': "macOS版本配置助手", 
            'linux': "Linux版本配置助手"
        }
        
        platform_desc = platform_info.get(self.target_platform, "跨平台版本")
        info_text = f"""欢迎使用墨问MCP社区版服务！({platform_desc})

请按以下步骤完成配置：
1. 获取您的墨问 API Key（个人中心 -> 开发者）
2. 在下方输入 API Key 并点击生成配置
3. 将生成的配置复制到 Trae 或 Cursor 等客户端的 MCP 设置中"""
        
        info_label = tk.Label(main_frame, text=info_text, 
                             font=("Arial", 10), justify=tk.LEFT)
        info_label.pack(anchor=tk.W, pady=(0, 20))
        
        # API Key输入区域
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(input_frame, text="API Key:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.api_entry = tk.Entry(input_frame, font=("Courier", 10), show="*", width=40)
        self.api_entry.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
        
        generate_btn = tk.Button(input_frame, text="生成配置", 
                               command=self.generate_config,
                               font=("Arial", 10), bg="#4CAF50", fg="white")
        generate_btn.pack(side=tk.RIGHT)
        
        # 配置显示区域
        tk.Label(main_frame, text="生成的配置:", 
                font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
        
        self.config_text = scrolledtext.ScrolledText(main_frame, height=15, 
                                                   font=("Courier", 9))
        self.config_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 按钮区域
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        copy_btn = tk.Button(button_frame, text="📋 复制到剪贴板", 
                           command=self.copy_config,
                           font=("Arial", 10), bg="#2196F3", fg="white")
        copy_btn.pack(side=tk.LEFT)
        
        save_btn = tk.Button(button_frame, text="💾 保存到文件", 
                           command=self.save_config,
                           font=("Arial", 10), bg="#FF9800", fg="white")
        save_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # 初始提示
        self.config_text.insert(tk.END, "请输入API Key并点击“生成配置”按钮...")
        
    def generate_config(self):
        """生成配置"""
        api_key = self.api_entry.get().strip()
        if not api_key:
            messagebox.showwarning("提示", "请输入API Key")
            return
            
        # 根据平台确定可执行文件路径
        if self.target_platform == 'windows':
            exe_name = "mowen-mcp-server.exe"
        else:
            exe_name = "mowen-mcp-server"
            
        exe_path = os.path.join(self.exe_dir, exe_name)
        
        # 路径标准化
        if self.target_platform != 'windows':
            exe_path = exe_path.replace('\\', '/')
        
        config = {
            "mcpServers": {
                "mowen-mcp-server": {
                    "command": exe_path,
                    "args": [],
                    "env": {
                        "MOWEN_API_KEY": api_key
                    }
                }
            }
        }
        
        config_json = json.dumps(config, indent=2, ensure_ascii=False)
        
        # 显示配置
        self.config_text.delete(1.0, tk.END)
        self.config_text.insert(tk.END, config_json)
        
        messagebox.showinfo("成功", "✅ 配置生成成功！\n\n请复制配置到Trae或Cursor等客户端的MCP设置中")
        
    def copy_config(self):
        """复制配置到剪贴板"""
        config_content = self.config_text.get(1.0, tk.END).strip()
        if not config_content or "请输入API Key" in config_content:
            messagebox.showwarning("提示", "请先生成配置")
            return
            
        self.root.clipboard_clear()
        self.root.clipboard_append(config_content)
        messagebox.showinfo("成功", "✅ 配置已复制到剪贴板！")
        
    def save_config(self):
        """保存配置到文件"""
        config_content = self.config_text.get(1.0, tk.END).strip()
        if not config_content or "请输入API Key" in config_content:
            messagebox.showwarning("提示", "请先生成配置")
            return
            
        try:
            config_file = os.path.join(self.exe_dir, "cursor_mcp_config.json")
            with open(config_file, "w", encoding="utf-8") as f:
                f.write(config_content)
            messagebox.showinfo("成功", f"✅ 配置已保存到:\n{config_file}")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ConfigHelper()
    app.run()