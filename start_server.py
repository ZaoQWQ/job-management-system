import http.server
import socketserver
import webbrowser
import threading
import time
import os

# 设置服务器端口
PORT = 8000

# 获取当前目录作为服务器根目录
handler = http.server.SimpleHTTPRequestHandler

# 创建TCP服务器
with socketserver.TCPServer(("localhost", PORT), handler) as httpd:
    print(f"服务器运行在 http://localhost:{PORT}")
    print(f"请在浏览器中打开: http://localhost:{PORT}/job_tracker.html")
    print("按 Ctrl+C 停止服务器")
    
    # 尝试在默认浏览器中打开页面
    try:
        webbrowser.open(f"http://localhost:{PORT}/job_tracker.html")
    except Exception as e:
        print(f"无法自动打开浏览器: {e}")
    
    # 运行服务器
    httpd.serve_forever()