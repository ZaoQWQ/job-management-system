#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Git操作工具
功能：提供代码库的创建、拉取、推送、克隆等Git操作
使用说明：直接运行脚本进入交互式界面，或作为模块导入使用
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def check_git_installed():
    """检查Git是否已安装"""
    try:
        subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def check_and_install_gitpython():
    """检查并安装GitPython库"""
    try:
        import git
        return True
    except ImportError:
        print("正在安装GitPython库...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gitpython'])
            print("GitPython安装成功")
            return True
        except subprocess.CalledProcessError:
            print("GitPython安装失败，请手动运行: pip install gitpython")
            return False

# 尝试导入git模块，如果失败则使用subprocess作为备用
_gitpython_available = False
try:
    import git
    _gitpython_available = True
except ImportError:
    pass

class GitOperations:
    """Git操作类"""
    
    def __init__(self):
        """初始化Git操作类"""
        self.current_repo = None
        self.current_path = os.getcwd()
    
    def create_repo(self, repo_path, initialize=True, create_readme=True):
        """
        在指定路径创建新的Git仓库
        
        Args:
            repo_path: 仓库路径
            initialize: 是否初始化Git仓库
            create_readme: 是否创建README.md文件
            
        Returns:
            bool: 操作是否成功
        """
        try:
            # 确保路径存在
            if not os.path.exists(repo_path):
                os.makedirs(repo_path)
                print(f"创建目录: {repo_path}")
            
            # 切换到仓库目录
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            # 创建README文件
            if create_readme and not os.path.exists('README.md'):
                with open('README.md', 'w', encoding='utf-8') as f:
                    f.write(f"# {os.path.basename(repo_path)}\n\n")
                    f.write(f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                print("创建README.md文件")
            
            # 初始化Git仓库
            if initialize:
                if _gitpython_available:
                    git.Repo.init(repo_path)
                else:
                    subprocess.run(['git', 'init'], check=True)
                print("Git仓库初始化成功")
            
            # 配置.gitignore文件
            if not os.path.exists('.gitignore'):
                self._create_gitignore()
            
            # 如果有文件，进行初始提交
            if create_readme:
                self._add_and_commit('初始提交')
            
            print(f"仓库创建成功: {repo_path}")
            self.current_repo = repo_path
            self.current_path = repo_path
            
            # 切换回原目录
            os.chdir(original_dir)
            return True
        
        except Exception as e:
            print(f"创建仓库失败: {e}")
            # 切换回原目录
            os.chdir(original_dir)
            return False
    
    def clone_repo(self, repo_url, target_path=None, branch=None):
        """
        克隆远程仓库到本地
        
        Args:
            repo_url: 远程仓库URL
            target_path: 本地目标路径，默认为仓库名
            branch: 要克隆的分支
            
        Returns:
            bool: 操作是否成功
        """
        try:
            # 如果未指定目标路径，从URL中提取仓库名
            if target_path is None:
                repo_name = repo_url.split('/')[-1]
                if repo_name.endswith('.git'):
                    repo_name = repo_name[:-4]
                target_path = os.path.join(os.getcwd(), repo_name)
            
            print(f"正在克隆仓库: {repo_url}")
            print(f"目标路径: {target_path}")
            
            # 执行克隆操作
            if _gitpython_available:
                kwargs = {'to_path': target_path}
                if branch:
                    kwargs['branch'] = branch
                git.Repo.clone_from(repo_url, **kwargs)
            else:
                cmd = ['git', 'clone']
                if branch:
                    cmd.extend(['-b', branch])
                cmd.extend([repo_url, target_path])
                subprocess.run(cmd, check=True)
            
            print(f"仓库克隆成功: {target_path}")
            self.current_repo = target_path
            self.current_path = target_path
            return True
        
        except Exception as e:
            print(f"克隆仓库失败: {e}")
            return False
    
    def pull(self, repo_path=None, branch='master'):
        """
        从远程仓库拉取最新代码
        
        Args:
            repo_path: 本地仓库路径
            branch: 要拉取的分支
            
        Returns:
            bool: 操作是否成功
        """
        try:
            repo_path = repo_path or self.current_repo
            if not repo_path:
                print("请指定仓库路径或先设置当前仓库")
                return False
            
            if not os.path.exists(os.path.join(repo_path, '.git')):
                print(f"指定路径不是Git仓库: {repo_path}")
                return False
            
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            print(f"正在从远程拉取分支 {branch} 的最新代码...")
            
            if _gitpython_available:
                repo = git.Repo(repo_path)
                origin = repo.remotes.origin
                origin.pull(branch)
            else:
                subprocess.run(['git', 'pull', 'origin', branch], check=True)
            
            print("代码拉取成功")
            os.chdir(original_dir)
            return True
        
        except Exception as e:
            print(f"拉取代码失败: {e}")
            os.chdir(original_dir)
            return False
    
    def push(self, repo_path=None, branch='master', set_upstream=False, message=None):
        """
        推送代码到远程仓库
        
        Args:
            repo_path: 本地仓库路径
            branch: 要推送的分支
            set_upstream: 是否设置上游分支
            message: 提交信息，如果为None则不执行提交
            
        Returns:
            bool: 操作是否成功
        """
        try:
            repo_path = repo_path or self.current_repo
            if not repo_path:
                print("请指定仓库路径或先设置当前仓库")
                return False
            
            if not os.path.exists(os.path.join(repo_path, '.git')):
                print(f"指定路径不是Git仓库: {repo_path}")
                return False
            
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            # 如果提供了提交信息，则执行提交
            if message:
                if not self._add_and_commit(message):
                    os.chdir(original_dir)
                    return False
            
            # 执行推送
            print(f"正在推送分支 {branch} 到远程仓库...")
            
            if _gitpython_available:
                repo = git.Repo(repo_path)
                origin = repo.remotes.origin
                if set_upstream:
                    origin.push(f'{branch}:{branch}', set_upstream=True)
                else:
                    origin.push(branch)
            else:
                cmd = ['git', 'push']
                if set_upstream:
                    cmd.extend(['--set-upstream', 'origin', branch])
                else:
                    cmd.extend(['origin', branch])
                subprocess.run(cmd, check=True)
            
            print("代码推送成功")
            os.chdir(original_dir)
            return True
        
        except Exception as e:
            print(f"推送代码失败: {e}")
            os.chdir(original_dir)
            return False
    
    def add_remote(self, repo_path=None, remote_name='origin', remote_url=None):
        """
        添加远程仓库
        
        Args:
            repo_path: 本地仓库路径
            remote_name: 远程仓库名称，默认为'origin'
            remote_url: 远程仓库URL
            
        Returns:
            bool: 操作是否成功
        """
        try:
            repo_path = repo_path or self.current_repo
            if not repo_path:
                print("请指定仓库路径或先设置当前仓库")
                return False
            
            if not remote_url:
                print("请提供远程仓库URL")
                return False
            
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            print(f"添加远程仓库 {remote_name}: {remote_url}")
            
            if _gitpython_available:
                repo = git.Repo(repo_path)
                repo.create_remote(remote_name, remote_url)
            else:
                subprocess.run(['git', 'remote', 'add', remote_name, remote_url], check=True)
            
            print(f"远程仓库 {remote_name} 添加成功")
            os.chdir(original_dir)
            return True
        
        except Exception as e:
            print(f"添加远程仓库失败: {e}")
            os.chdir(original_dir)
            return False
    
    def set_current_repo(self, repo_path):
        """
        设置当前操作的仓库
        
        Args:
            repo_path: 仓库路径
            
        Returns:
            bool: 操作是否成功
        """
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print(f"指定路径不是Git仓库: {repo_path}")
            return False
        
        self.current_repo = repo_path
        self.current_path = repo_path
        print(f"当前仓库已设置为: {repo_path}")
        return True
    
    def status(self, repo_path=None):
        """
        查看仓库状态
        
        Args:
            repo_path: 仓库路径
            
        Returns:
            bool: 操作是否成功
        """
        try:
            repo_path = repo_path or self.current_repo
            if not repo_path:
                print("请指定仓库路径或先设置当前仓库")
                return False
            
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            if _gitpython_available:
                repo = git.Repo(repo_path)
                print("仓库状态:")
                print(f"当前分支: {repo.active_branch.name}")
                print("\n未跟踪的文件:")
                for file in repo.untracked_files:
                    print(f"  - {file}")
                print("\n修改的文件:")
                for item in repo.index.diff(None):
                    print(f"  - {item.a_path}")
                print("\n已暂存的文件:")
                for item in repo.index.diff('HEAD'):
                    print(f"  - {item.a_path}")
            else:
                result = subprocess.run(['git', 'status'], check=True, capture_output=True, text=True)
                print(result.stdout)
            
            os.chdir(original_dir)
            return True
        
        except Exception as e:
            print(f"查看仓库状态失败: {e}")
            os.chdir(original_dir)
            return False
    
    def commit(self, repo_path=None, message='更新'):
        """
        提交更改
        
        Args:
            repo_path: 仓库路径
            message: 提交信息
            
        Returns:
            bool: 操作是否成功
        """
        return self._add_and_commit(message, repo_path)
    
    def _add_and_commit(self, message, repo_path=None):
        """
        添加所有文件并提交
        
        Args:
            message: 提交信息
            repo_path: 仓库路径
            
        Returns:
            bool: 操作是否成功
        """
        try:
            repo_path = repo_path or self.current_repo
            if not repo_path:
                print("请指定仓库路径或先设置当前仓库")
                return False
            
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            if _gitpython_available:
                repo = git.Repo(repo_path)
                repo.git.add('.')
                repo.git.commit('-m', message)
            else:
                subprocess.run(['git', 'add', '.'], check=True)
                subprocess.run(['git', 'commit', '-m', message], check=True)
            
            print(f"提交成功: {message}")
            os.chdir(original_dir)
            return True
        
        except Exception as e:
            print(f"提交失败: {e}")
            os.chdir(original_dir)
            return False
    
    def _create_gitignore(self):
        """创建.gitignore文件"""
        gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Database
*.db
*.sqlite3

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Editor directories and files
.vscode/
.idea/
*.swp
*.swo
*~

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
*.log
logs/

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Virtual environments
venv/
env/
pyvenv/
env3/

# Flask
*.pyc
instance/
.cache/

# Testing
coverage/
.pytest_cache/

# Distribution / packaging
build/
dist/
eggs/
*.egg-info/'''
        
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("创建.gitignore文件")

def display_menu():
    """显示菜单"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 50)
    print("        Git操作工具        ")
    print("=" * 50)
    print("1. 创建新的Git仓库")
    print("2. 克隆远程仓库")
    print("3. 拉取远程代码")
    print("4. 推送代码到远程")
    print("5. 添加远程仓库")
    print("6. 查看仓库状态")
    print("7. 设置当前仓库")
    print("8. 提交更改")
    print("0. 退出系统")
    print("=" * 50)

def main():
    """主函数"""
    # 检查Git是否安装
    if not check_git_installed():
        print("错误: 未检测到Git，请先安装Git")
        print("Windows用户可以从 https://git-scm.com/downloads 下载安装")
        print("Linux用户可以使用包管理器安装: apt-get install git 或 yum install git")
        input("按回车键退出...")
        return
    
    # 检查并尝试安装GitPython
    check_and_install_gitpython()
    
    git_ops = GitOperations()
    
    while True:
        display_menu()
        choice = input("请输入操作编号: ").strip()
        
        if choice == '1':
            # 创建新仓库
            repo_path = input("请输入仓库路径 (默认为当前目录): ").strip() or os.getcwd()
            if git_ops.create_repo(repo_path):
                input("\n仓库创建成功！按回车键继续...")
            else:
                input("\n按回车键继续...")
        
        elif choice == '2':
            # 克隆仓库
            repo_url = input("请输入远程仓库URL: ").strip()
            if repo_url:
                target_path = input("请输入本地目标路径 (可选): ").strip() or None
                branch = input("请输入要克隆的分支 (可选): ").strip() or None
                if git_ops.clone_repo(repo_url, target_path, branch):
                    input("\n仓库克隆成功！按回车键继续...")
                else:
                    input("\n按回车键继续...")
            else:
                input("\nURL不能为空！按回车键继续...")
        
        elif choice == '3':
            # 拉取代码
            repo_path = input("请输入仓库路径 (默认为当前仓库): ").strip() or None
            branch = input("请输入分支名称 (默认为master): ").strip() or 'master'
            if git_ops.pull(repo_path, branch):
                input("\n代码拉取成功！按回车键继续...")
            else:
                input("\n按回车键继续...")
        
        elif choice == '4':
            # 推送代码
            repo_path = input("请输入仓库路径 (默认为当前仓库): ").strip() or None
            branch = input("请输入分支名称 (默认为master): ").strip() or 'master'
            message = input("请输入提交信息 (可选，留空则只推送不提交): ").strip() or None
            
            # 询问是否设置上游分支
            set_upstream_input = input("是否设置上游分支？(y/n，默认为n): ").strip().lower()
            set_upstream = set_upstream_input == 'y'
            
            if git_ops.push(repo_path, branch, set_upstream, message):
                input("\n代码推送成功！按回车键继续...")
            else:
                input("\n按回车键继续...")
        
        elif choice == '5':
            # 添加远程仓库
            repo_path = input("请输入仓库路径 (默认为当前仓库): ").strip() or None
            remote_name = input("请输入远程仓库名称 (默认为origin): ").strip() or 'origin'
            remote_url = input("请输入远程仓库URL: ").strip()
            
            if remote_url:
                if git_ops.add_remote(repo_path, remote_name, remote_url):
                    input("\n远程仓库添加成功！按回车键继续...")
                else:
                    input("\n按回车键继续...")
            else:
                input("\nURL不能为空！按回车键继续...")
        
        elif choice == '6':
            # 查看仓库状态
            repo_path = input("请输入仓库路径 (默认为当前仓库): ").strip() or None
            git_ops.status(repo_path)
            input("\n按回车键继续...")
        
        elif choice == '7':
            # 设置当前仓库
            repo_path = input("请输入仓库路径: ").strip()
            if repo_path:
                git_ops.set_current_repo(repo_path)
            else:
                print("路径不能为空！")
            input("\n按回车键继续...")
        
        elif choice == '8':
            # 提交更改
            repo_path = input("请输入仓库路径 (默认为当前仓库): ").strip() or None
            message = input("请输入提交信息 (默认为'更新'): ").strip() or '更新'
            if git_ops.commit(repo_path, message):
                input("\n提交成功！按回车键继续...")
            else:
                input("\n按回车键继续...")
        
        elif choice == '0':
            print("\n感谢使用Git操作工具，再见！")
            time.sleep(1)
            break
        
        else:
            print("\n无效的操作编号，请重新输入")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序发生错误: {e}")
        input("按回车键退出...")