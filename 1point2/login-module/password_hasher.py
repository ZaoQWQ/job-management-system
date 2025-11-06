import bcrypt

class PasswordHasher:
    """密码处理类，仅负责密码的哈希和验证"""
    
    def hash_password(self, password):
        """对密码进行哈希处理"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """验证密码与哈希值是否匹配"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
