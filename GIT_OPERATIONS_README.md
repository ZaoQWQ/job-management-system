# Git操作工具

一个功能完整的Git仓库管理工具，提供代码库的创建、拉取、推送、克隆等操作的命令行界面。

## 功能特性

- ✅ **创建仓库**: 在指定路径创建新的Git仓库，自动初始化并创建README和.gitignore文件
- ✅ **克隆仓库**: 从远程URL克隆仓库到本地，可以指定分支
- ✅ **拉取代码**: 从远程仓库拉取最新代码到本地
- ✅ **推送代码**: 将本地代码提交并推送到远程仓库
- ✅ **添加远程**: 为本地仓库添加远程仓库连接
- ✅ **查看状态**: 查看当前仓库的Git状态
- ✅ **提交更改**: 提交本地修改到版本历史
- ✅ **设置当前仓库**: 设置默认操作的仓库路径

## 系统要求

- Python 3.6+
- Git（请确保已安装并添加到系统PATH）

## 安装依赖

工具会自动检查并尝试安装GitPython库。如果自动安装失败，可以手动安装：

```bash
pip install gitpython
```

## 使用方法

### 方法1：交互式界面

直接运行主程序进入交互式界面：

```bash
python git_operations.py
```

然后按照菜单提示输入相应的操作编号，按照引导完成Git操作。

### 方法2：作为模块导入

也可以将工具作为Python模块导入到您的项目中使用：

```python
from git_operations import GitOperations

# 创建Git操作实例
git_ops = GitOperations()

# 创建新仓库
git_ops.create_repo("/path/to/new/repo")

# 克隆仓库
git_ops.clone_repo("https://github.com/username/repo.git")

# 拉取代码
git_ops.pull("/path/to/repo", "main")

# 推送代码
git_ops.push("/path/to/repo", "main", message="更新内容")
```

## 测试工具

运行测试脚本来验证基本功能是否正常：

```bash
python test_git_operations.py
```

测试脚本会自动：
1. 检查Git和GitPython是否安装
2. 创建一个测试仓库
3. 验证基本的Git操作功能

## 注意事项

1. **权限问题**：确保您对操作的目录有读写权限
2. **远程仓库**：操作远程仓库时，请确保您有相应的访问权限（SSH密钥或用户名密码）
3. **网络连接**：克隆、拉取、推送操作需要网络连接
4. **分支名称**：默认使用'master'分支，可根据需要指定其他分支

## 错误处理

工具会显示详细的错误信息，常见问题解决方法：

- **Git未安装**：请从 [Git官网](https://git-scm.com/downloads) 下载并安装
- **权限错误**：检查文件系统权限和远程仓库访问权限
- **网络错误**：检查网络连接和远程仓库URL是否正确
- **认证失败**：确保SSH密钥配置正确或用户名密码输入正确

## 文件结构

- `git_operations.py` - 主程序文件，包含所有Git操作功能
- `test_git_operations.py` - 测试脚本，用于验证基本功能

## 许可证

本工具为开源软件，可以自由使用和修改。

## 版本历史

### v1.0
- 初始版本
- 实现基本的Git操作功能
- 提供交互式界面和模块导入两种使用方式
- 支持自动依赖检查和安装