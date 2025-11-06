from flask import Flask
from login_controller import LoginController
from login_service import LoginService
from user_repository import UserRepository
from password_hasher import PasswordHasher

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'login_system'
}

def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    
    # 初始化组件
    password_hasher = PasswordHasher()
    user_repository = UserRepository(DB_CONFIG)
    login_service = LoginService(user_repository, password_hasher)
    login_controller = LoginController(login_service)
    
    # 注册路由
    app.add_url_rule(
        '/api/login', 
        view_func=login_controller.handle_login_request, 
        methods=['POST']
    )
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
