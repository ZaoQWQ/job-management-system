class LoginService:
    """登录服务类，仅负责处理登录业务逻辑"""
    
    def __init__(self, user_repository, password_hasher):
        # 依赖注入，不直接创建依赖对象，提高可测试性
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        
    def login(self, username, password, ip_address, user_agent):
        """
        处理登录逻辑
        返回: 成功时返回用户对象，失败时返回None
        """
        # 查找用户
        user = self.user_repository.find_by_username(username)
        user_id = user.id if user else None
        
        # 验证用户是否存在
        if not user:
            self.user_repository.log_login_attempt(
                user_id, ip_address, user_agent, False, "用户名不存在"
            )
            return None
        
        # 验证密码
        if not self.password_hasher.verify_password(password, user.get_password_hash()):
            self.user_repository.log_login_attempt(
                user_id, ip_address, user_agent, False, "密码不正确"
            )
            return None
        
        # 登录成功，更新最后登录时间并记录日志
        self.user_repository.update_last_login(user.get_id())
        self.user_repository.log_login_attempt(
            user_id, ip_address, user_agent, True
        )
        
        return user
