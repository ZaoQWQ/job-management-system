#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Git操作测试脚本
用于测试git_operations.py中的基本功能
"""

import os
import sys
import time
from git_operations import GitOperations, check_git_installed, check_and_install_gitpython

def main():
    """测试Git操作功能"""
    print("Git操作功能测试")
    print("=" * 50)
    
    # 检查Git是否安装
    if not check_git_installed():
        print("✗ Git未安装，请先安装Git")
        return
    else:
        print("✓ Git已安装")
    
    # 检查GitPython
    gitpython_available = check_and_install_gitpython()
    print(f"✓ GitPython可用: {gitpython_available}")
    
    # 创建GitOperations实例
    git_ops = GitOperations()
    print("✓ GitOperations实例创建成功")
    
    # 测试目录操作
    test_dir = os.path.join(os.getcwd(), "test_git_repo")
    print(f"\n测试目录: {test_dir}")
    
    # 清理之前的测试目录
    if os.path.exists(test_dir):
        import shutil
        try:
            shutil.rmtree(test_dir)
            print("✓ 已清理之前的测试目录")
        except Exception as e:
            print(f"✗ 清理测试目录失败: {e}")
    
    # 测试创建仓库
    print("\n测试创建仓库...")
    if git_ops.create_repo(test_dir, initialize=True, create_readme=True):
        print("✓ 仓库创建成功")
        
        # 测试状态查看
        print("\n测试查看仓库状态...")
        git_ops.status(test_dir)
        
        # 创建一个测试文件
        test_file_path = os.path.join(test_dir, "test_file.txt")
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("这是一个测试文件\n")
        print(f"\n✓ 已创建测试文件: {test_file_path}")
        
        # 测试提交
        print("\n测试提交更改...")
        if git_ops.commit(test_dir, "添加测试文件"):
            print("✓ 提交成功")
        
        # 再次查看状态
        print("\n再次查看仓库状态:")
        git_ops.status(test_dir)
    else:
        print("✗ 仓库创建失败")
    
    print("\n" + "=" * 50)
    print("测试完成！您可以使用主程序 git_operations.py 进行完整的Git操作")
    print("运行方法: python git_operations.py")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
    except Exception as e:
        print(f"\n测试发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("按回车键退出...")