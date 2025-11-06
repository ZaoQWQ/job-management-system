from flask import request, jsonify

class LoginController:
    """登录控制器类，仅负责处理HTTP请求和响应"""
    
    def __init__(self, login_service):
        self.login_service = login_service
        
    def handle_login_request(self):
        """处理登录HTTP请求"""
        # 获取请求数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # 验证请求数据
        if not username or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码不能为空'
            }), 400
        
        # 获取客户端信息
        ip_address = request.remote_addr
        user_agent = request.user_agent.string
        
        # 调用服务层处理业务逻辑
        user = self.login_service.login(username, password, ip_address, user_agent)
        
        # 构建并返回响应
        if user:
            return jsonify({
                'success': True,
                'message': '登录成功',
                'data': {
                    'user_id': user.get_id(),
                    'username': user.get_username(),
                    'email': user.get_email()
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': '用户名或密码不正确'
            }), 401
