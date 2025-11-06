class User:
    """用户模型类，仅负责存储和提供用户数据"""
    
    def __init__(self, user_id, username, password_hash, email):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        
    def get_id(self):
        return self.id
        
    def get_username(self):
        return self.username
        
    def get_password_hash(self):
        return self.password_hash
        
    def get_email(self):
        return self.email
