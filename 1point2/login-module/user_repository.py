import mysql.connector
from user import User

class UserRepository:
    """用户数据访问类，仅负责与数据库交互"""
    
    def __init__(self, db_config):
        self.db_config = db_config
        
    def _get_connection(self):
        """创建并返回数据库连接"""
        return mysql.connector.connect(
            host=self.db_config['host'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database']
        )
    
    def find_by_username(self, username):
        """根据用户名查找用户"""
        connection = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, username, password_hash, email FROM users WHERE username = %s", (username,))
            user_data = cursor.fetchone()
            
            if user_data:
                return User(
                    user_id=user_data['id'],
                    username=user_data['username'],
                    password_hash=user_data['password_hash'],
                    email=user_data['email']
                )
            return None
        finally:
            if connection:
                connection.close()
    
    def update_last_login(self, user_id):
        """更新用户最后登录时间"""
        connection = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s", 
                (user_id,)
            )
            connection.commit()
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"更新最后登录时间失败: {str(e)}")
            return False
        finally:
            if connection:
                connection.close()
    
    def log_login_attempt(self, user_id, ip_address, user_agent, success, error_message=None):
        """记录登录尝试信息"""
        connection = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO login_logs 
                   (user_id, ip_address, user_agent, success, error_message) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (user_id, ip_address, user_agent, success, error_message)
            )
            connection.commit()
            return True
        except Exception as e:
            if connection:
                connection.rollback()
            print(f"记录登录日志失败: {str(e)}")
            return False
        finally:
            if connection:
                connection.close()
