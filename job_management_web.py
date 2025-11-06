#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
岗位管理系统 - 网页版
功能：训练学生使用数据库的增删改查(CRUD)操作
包含：岗位的添加、列表展示、筛选查询、删除和修改功能
使用Flask框架实现Web界面
"""

import sqlite3
import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# 创建Flask应用实例
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于flash消息的安全密钥

# 数据库文件名
DB_FILE = 'job_management.db'

# 初始化数据库表（仅在应用启动时执行一次）
def init_database():
    """初始化数据库并创建表"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        salary TEXT,
        requirements TEXT,
        location TEXT,
        posted_date DATE DEFAULT CURRENT_DATE,
        description TEXT,
        contact_person TEXT,
        contact_phone TEXT,
        email TEXT
    );
    '''
    
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print("岗位表创建成功")
    except sqlite3.Error as e:
        print(f"创建表失败: {e}")
        conn.rollback()
    finally:
        conn.close()

# 获取数据库连接（为每个请求创建独立连接）
def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # 允许通过列名访问
    return conn

# 确保数据库连接在请求结束后关闭
@app.teardown_appcontext
def close_connection(exception):
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.close()
    except:
        pass

@app.route('/')
def index():
    """首页，显示岗位列表"""
    # 获取筛选参数
    company_name = request.args.get('company_name', '').strip()
    job_title = request.args.get('job_title', '').strip()
    location = request.args.get('location', '').strip()
    
    # 构建查询SQL
    base_query = """
    SELECT id, company_name, job_title, salary, location, posted_date 
    FROM jobs
    """
    
    conditions = []
    params = []
    
    if company_name:
        conditions.append("company_name LIKE ?")
        params.append(f"%{company_name}%")
    if job_title:
        conditions.append("job_title LIKE ?")
        params.append(f"%{job_title}%")
    if location:
        conditions.append("location LIKE ?")
        params.append(f"%{location}%")
    
    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    
    base_query += " ORDER BY posted_date DESC"
    
    # 获取数据库连接
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(base_query, params)
        jobs = cursor.fetchall()
        
        # 将结果转换为字典列表，方便模板使用
        job_list = []
        for job in jobs:
            job_list.append({
                'id': job[0],
                'company_name': job[1],
                'job_title': job[2],
                'salary': job[3] or '',
                'location': job[4] or '',
                'posted_date': job[5]
            })
        
        return render_template('index.html', jobs=job_list, 
                             company_name=company_name, 
                             job_title=job_title, 
                             location=location)
    except sqlite3.Error as e:
        flash(f"查询岗位失败: {str(e)}")
        return render_template('index.html', jobs=[])
    finally:
        conn.close()

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    """添加新岗位"""
    if request.method == 'POST':
        # 获取表单数据
        company_name = request.form.get('company_name', '').strip()
        job_title = request.form.get('job_title', '').strip()
        salary = request.form.get('salary', '').strip()
        requirements = request.form.get('requirements', '').strip()
        location = request.form.get('location', '').strip()
        description = request.form.get('description', '').strip()
        contact_person = request.form.get('contact_person', '').strip()
        contact_phone = request.form.get('contact_phone', '').strip()
        email = request.form.get('email', '').strip()
        
        # 验证必填字段
        if not company_name:
            flash('企业名称不能为空')
            return render_template('add_job.html')
        if not job_title:
            flash('岗位名称不能为空')
            return render_template('add_job.html')
        
        # 插入数据
        insert_sql = '''
        INSERT INTO jobs (company_name, job_title, salary, requirements, location, 
                         description, contact_person, contact_phone, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        # 获取数据库连接
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(insert_sql, (
                company_name, job_title, salary, requirements, location,
                description, contact_person, contact_phone, email
            ))
            conn.commit()
            flash(f"岗位添加成功！ID: {cursor.lastrowid}")
            return redirect(url_for('index'))
        except sqlite3.Error as e:
            flash(f"添加岗位失败: {str(e)}")
            return render_template('add_job.html')
        finally:
            conn.close()
    
    return render_template('add_job.html')

@app.route('/view_job/<int:job_id>')
def view_job(job_id):
    """查看岗位详细信息"""
    select_sql = """
    SELECT * FROM jobs WHERE id = ?
    """
    
    # 获取数据库连接
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(select_sql, (job_id,))
        job = cursor.fetchone()
        
        if not job:
            flash(f"未找到ID为 {job_id} 的岗位")
            return redirect(url_for('index'))
        
        # 将结果转换为字典
        job_details = {
            'id': job[0],
            'company_name': job[1],
            'job_title': job[2],
            'salary': job[3] or '未填写',
            'requirements': job[4] or '未填写',
            'location': job[5] or '未填写',
            'posted_date': job[6],
            'description': job[7] or '未填写',
            'contact_person': job[8] or '未填写',
            'contact_phone': job[9] or '未填写',
            'email': job[10] or '未填写'
        }
        
        return render_template('view_job.html', job=job_details)
    except sqlite3.Error as e:
        flash(f"查询岗位详情失败: {str(e)}")
        return redirect(url_for('index'))
    finally:
        conn.close()

@app.route('/update_job/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    """更新岗位信息"""
    if request.method == 'POST':
        # 获取表单数据
        company_name = request.form.get('company_name', '').strip()
        job_title = request.form.get('job_title', '').strip()
        salary = request.form.get('salary', '').strip()
        requirements = request.form.get('requirements', '').strip()
        location = request.form.get('location', '').strip()
        description = request.form.get('description', '').strip()
        contact_person = request.form.get('contact_person', '').strip()
        contact_phone = request.form.get('contact_phone', '').strip()
        email = request.form.get('email', '').strip()
        
        # 验证必填字段
        if not company_name:
            flash('企业名称不能为空')
            return redirect(url_for('update_job', job_id=job_id))
        if not job_title:
            flash('岗位名称不能为空')
            return redirect(url_for('update_job', job_id=job_id))
        
        # 更新数据
        update_sql = '''
        UPDATE jobs SET company_name=?, job_title=?, salary=?, requirements=?, location=?,
                       description=?, contact_person=?, contact_phone=?, email=?
        WHERE id=?
        '''
        
        # 获取数据库连接
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(update_sql, (
                company_name, job_title, salary, requirements, location,
                description, contact_person, contact_phone, email, job_id
            ))
            conn.commit()
            flash(f"岗位 {job_id} 更新成功！")
            return redirect(url_for('view_job', job_id=job_id))
        except sqlite3.Error as e:
            flash(f"更新岗位失败: {str(e)}")
            return redirect(url_for('update_job', job_id=job_id))
        finally:
            conn.close()
    
    # GET 请求：获取岗位当前信息
    select_sql = """
    SELECT * FROM jobs WHERE id = ?
    """
    
    # 获取数据库连接
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(select_sql, (job_id,))
        job = cursor.fetchone()
        
        if not job:
            flash(f"未找到ID为 {job_id} 的岗位")
            return redirect(url_for('index'))
        
        # 将结果转换为字典
        job_details = {
            'id': job[0],
            'company_name': job[1],
            'job_title': job[2],
            'salary': job[3] or '',
            'requirements': job[4] or '',
            'location': job[5] or '',
            'posted_date': job[6],
            'description': job[7] or '',
            'contact_person': job[8] or '',
            'contact_phone': job[9] or '',
            'email': job[10] or ''
        }
        
        return render_template('update_job.html', job=job_details)
    except sqlite3.Error as e:
        flash(f"查询岗位详情失败: {str(e)}")
        return redirect(url_for('index'))
    finally:
        conn.close()

@app.route('/delete_job/<int:job_id>', methods=['GET', 'POST'])
def delete_job(job_id):
    """删除岗位"""
    if request.method == 'POST':
        # 执行删除操作
        delete_sql = "DELETE FROM jobs WHERE id = ?"
        
        # 获取数据库连接
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(delete_sql, (job_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                flash(f"岗位 {job_id} 已成功删除！")
            else:
                flash(f"未找到ID为 {job_id} 的岗位")
                
            return redirect(url_for('index'))
        except sqlite3.Error as e:
            flash(f"删除岗位失败: {str(e)}")
            return redirect(url_for('index'))
        finally:
            conn.close()
    
    # GET 请求：显示确认页面
    select_sql = """
    SELECT id, company_name, job_title FROM jobs WHERE id = ?
    """
    
    # 获取数据库连接
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(select_sql, (job_id,))
        job = cursor.fetchone()
        
        if not job:
            flash(f"未找到ID为 {job_id} 的岗位")
            return redirect(url_for('index'))
        
        job_details = {
            'id': job[0],
            'company_name': job[1],
            'job_title': job[2]
        }
        
        return render_template('delete_job.html', job=job_details)
    except sqlite3.Error as e:
        flash(f"查询岗位详情失败: {str(e)}")
        return redirect(url_for('index'))
    finally:
        conn.close()

# API接口，用于异步操作
@app.route('/api/jobs', methods=['GET'])
def api_jobs():
    """获取岗位列表的API接口"""
    # 获取数据库连接
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, company_name, job_title, salary, location, posted_date FROM jobs ORDER BY posted_date DESC")
        jobs = cursor.fetchall()
        
        # 转换为JSON格式
        result = []
        for job in jobs:
            result.append({
                'id': job[0],
                'company_name': job[1],
                'job_title': job[2],
                'salary': job[3] or '未填写',
                'location': job[4] or '未填写',
                'posted_date': job[5]
            })
        
        return jsonify({'success': True, 'data': result})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/job/<int:job_id>', methods=['GET'])
def api_job(job_id):
    """获取单个岗位详情的API接口"""
    # 获取数据库连接
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        job = cursor.fetchone()
        
        if not job:
            return jsonify({'error': '岗位不存在'}), 404
        
        # 转换为JSON格式
        result = {
            'id': job[0],
            'company_name': job[1],
            'job_title': job[2],
            'salary': job[3] or '未填写',
            'requirements': job[4] or '未填写',
            'location': job[5] or '未填写',
            'posted_date': job[6],
            'description': job[7] or '未填写',
            'contact_person': job[8] or '未填写',
            'contact_phone': job[9] or '未填写',
            'email': job[10] or '未填写'
        }
        
        return jsonify({'success': True, 'data': result})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# 创建模板目录和HTML文件
def create_templates():
    """创建必要的模板目录和HTML文件"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    
    # 创建templates目录
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"创建模板目录: {templates_dir}")
    
    # 基础模板
    base_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}岗位管理系统{% endblock %}</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background-color: #2c3e50;
            color: white;
            padding: 20px 0;
            margin-bottom: 30px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        header .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 {
            margin: 0;
            font-size: 24px;
        }
        nav a {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            margin-left: 10px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        nav a:hover {
            background-color: #34495e;
        }
        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            padding: 24px;
            margin-bottom: 20px;
        }
        h2 {
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
        }
        tr:hover {
            background-color: #f8f9fa;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
            transition: background-color 0.3s;
        }
        .btn-primary {
            background-color: #3498db;
            color: white;
        }
        .btn-primary:hover {
            background-color: #2980b9;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background-color: #5a6268;
        }
        .btn-danger {
            background-color: #dc3545;
            color: white;
        }
        .btn-danger:hover {
            background-color: #c82333;
        }
        .btn-success {
            background-color: #28a745;
            color: white;
        }
        .btn-success:hover {
            background-color: #218838;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        .messages {
            margin-bottom: 20px;
        }
        .message {
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 4px;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .actions {
            display: flex;
            gap: 10px;
        }
        .filter-form {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .filter-form .form-group {
            flex: 1;
            min-width: 200px;
            margin-bottom: 0;
        }
        .filter-form button {
            align-self: flex-end;
        }
        .detail-item {
            margin-bottom: 15px;
        }
        .detail-label {
            font-weight: 600;
            color: #666;
            margin-bottom: 5px;
        }
        .detail-value {
            color: #333;
        }
        @media (max-width: 768px) {
            header .container {
                flex-direction: column;
                gap: 15px;
            }
            .filter-form {
                flex-direction: column;
            }
            table {
                font-size: 14px;
            }
            th, td {
                padding: 8px;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>岗位管理系统</h1>
            <nav>
                <a href="{{ url_for('index') }}">岗位列表</a>
                <a href="{{ url_for('add_job') }}">添加岗位</a>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <!-- 消息提示 -->
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        <div class="messages">
            {% for category, message in messages %}
            <div class="message {{ category }}">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}
        {% endwith %}
        
        <!-- 页面内容 -->
        <div class="card">
            {% block content %}{% endblock %}
        </div>
    </div>
</body>
</html>'''
    
    # 首页模板
    index_html = '''{% extends "base.html" %}
{% block title %}岗位列表 - 岗位管理系统{% endblock %}
{% block content %}
    <h2>岗位列表</h2>
    
    <!-- 筛选表单 -->
    <form action="{{ url_for('index') }}" method="get" class="filter-form">
        <div class="form-group">
            <label for="company_name">企业名称</label>
            <input type="text" id="company_name" name="company_name" value="{{ company_name }}" placeholder="输入企业名称搜索">
        </div>
        <div class="form-group">
            <label for="job_title">岗位名称</label>
            <input type="text" id="job_title" name="job_title" value="{{ job_title }}" placeholder="输入岗位名称搜索">
        </div>
        <div class="form-group">
            <label for="location">工作地点</label>
            <input type="text" id="location" name="location" value="{{ location }}" placeholder="输入工作地点搜索">
        </div>
        <div style="display: flex; gap: 10px; align-items: flex-end;">
            <button type="submit" class="btn btn-primary">搜索</button>
            <a href="{{ url_for('index') }}" class="btn btn-secondary">重置</a>
        </div>
    </form>
    
    <!-- 岗位列表表格 -->
    {% if jobs %}
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>企业名称</th>
                <th>岗位名称</th>
                <th>薪资</th>
                <th>工作地点</th>
                <th>发布日期</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            {% for job in jobs %}
            <tr>
                <td>{{ job.id }}</td>
                <td>{{ job.company_name }}</td>
                <td>{{ job.job_title }}</td>
                <td>{{ job.salary }}</td>
                <td>{{ job.location }}</td>
                <td>{{ job.posted_date }}</td>
                <td>
                    <div class="actions">
                        <a href="{{ url_for('view_job', job_id=job.id) }}" class="btn btn-secondary" style="padding: 5px 10px; font-size: 12px;">查看</a>
                        <a href="{{ url_for('update_job', job_id=job.id) }}" class="btn btn-primary" style="padding: 5px 10px; font-size: 12px;">编辑</a>
                        <a href="{{ url_for('delete_job', job_id=job.id) }}" class="btn btn-danger" style="padding: 5px 10px; font-size: 12px;">删除</a>
                    </div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="text-align: center; padding: 30px; color: #666;">暂无岗位记录</p>
    {% endif %}
{% endblock %}'''
    
    # 添加岗位模板
    add_job_html = '''{% extends "base.html" %}
{% block title %}添加岗位 - 岗位管理系统{% endblock %}
{% block content %}
    <h2>添加新岗位</h2>
    
    <form action="{{ url_for('add_job') }}" method="post">
        <div class="form-group">
            <label for="company_name">企业名称 <span style="color: red;">*</span></label>
            <input type="text" id="company_name" name="company_name" placeholder="请输入企业名称" required>
        </div>
        
        <div class="form-group">
            <label for="job_title">岗位名称 <span style="color: red;">*</span></label>
            <input type="text" id="job_title" name="job_title" placeholder="请输入岗位名称" required>
        </div>
        
        <div class="form-group">
            <label for="salary">薪资</label>
            <input type="text" id="salary" name="salary" placeholder="请输入薪资范围">
        </div>
        
        <div class="form-group">
            <label for="requirements">具体要求</label>
            <textarea id="requirements" name="requirements" placeholder="请输入岗位具体要求"></textarea>
        </div>
        
        <div class="form-group">
            <label for="location">工作地点</label>
            <input type="text" id="location" name="location" placeholder="请输入工作地点">
        </div>
        
        <div class="form-group">
            <label for="description">岗位描述</label>
            <textarea id="description" name="description" placeholder="请输入岗位详细描述"></textarea>
        </div>
        
        <div class="form-group">
            <label for="contact_person">联系人</label>
            <input type="text" id="contact_person" name="contact_person" placeholder="请输入联系人姓名">
        </div>
        
        <div class="form-group">
            <label for="contact_phone">联系电话</label>
            <input type="text" id="contact_phone" name="contact_phone" placeholder="请输入联系电话">
        </div>
        
        <div class="form-group">
            <label for="email">电子邮箱</label>
            <input type="text" id="email" name="email" placeholder="请输入电子邮箱">
        </div>
        
        <div class="actions">
            <button type="submit" class="btn btn-success">保存</button>
            <a href="{{ url_for('index') }}" class="btn btn-secondary">取消</a>
        </div>
    </form>
{% endblock %}'''
    
    # 查看岗位模板
    view_job_html = '''{% extends "base.html" %}
{% block title %}岗位详情 - 岗位管理系统{% endblock %}
{% block content %}
    <h2>岗位详情</h2>
    
    <div>
        <div class="detail-item">
            <div class="detail-label">ID</div>
            <div class="detail-value">{{ job.id }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">企业名称</div>
            <div class="detail-value">{{ job.company_name }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">岗位名称</div>
            <div class="detail-value">{{ job.job_title }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">薪资</div>
            <div class="detail-value">{{ job.salary }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">具体要求</div>
            <div class="detail-value">{{ job.requirements }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">工作地点</div>
            <div class="detail-value">{{ job.location }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">发布日期</div>
            <div class="detail-value">{{ job.posted_date }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">岗位描述</div>
            <div class="detail-value">{{ job.description }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">联系人</div>
            <div class="detail-value">{{ job.contact_person }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">联系电话</div>
            <div class="detail-value">{{ job.contact_phone }}</div>
        </div>
        
        <div class="detail-item">
            <div class="detail-label">电子邮箱</div>
            <div class="detail-value">{{ job.email }}</div>
        </div>
        
        <div class="actions" style="margin-top: 30px;">
            <a href="{{ url_for('update_job', job_id=job.id) }}" class="btn btn-primary">编辑</a>
            <a href="{{ url_for('delete_job', job_id=job.id) }}" class="btn btn-danger">删除</a>
            <a href="{{ url_for('index') }}" class="btn btn-secondary">返回列表</a>
        </div>
    </div>
{% endblock %}'''
    
    # 更新岗位模板
    update_job_html = '''{% extends "base.html" %}
{% block title %}更新岗位 - 岗位管理系统{% endblock %}
{% block content %}
    <h2>更新岗位信息</h2>
    
    <form action="{{ url_for('update_job', job_id=job[0]) }}" method="post">
        <div class="form-group">
            <label for="company_name">企业名称 <span style="color: red;">*</span></label>
            <input type="text" id="company_name" name="company_name" value="{{ job[1] }}" required>
        </div>
        
        <div class="form-group">
            <label for="job_title">岗位名称 <span style="color: red;">*</span></label>
            <input type="text" id="job_title" name="job_title" value="{{ job[2] }}" required>
        </div>
        
        <div class="form-group">
            <label for="salary">薪资</label>
            <input type="text" id="salary" name="salary" value="{{ job[3] or '' }}">
        </div>
        
        <div class="form-group">
            <label for="requirements">具体要求</label>
            <textarea id="requirements" name="requirements">{{ job[4] or '' }}</textarea>
        </div>
        
        <div class="form-group">
            <label for="location">工作地点</label>
            <input type="text" id="location" name="location" value="{{ job[5] or '' }}">
        </div>
        
        <div class="form-group">
            <label for="description">岗位描述</label>
            <textarea id="description" name="description">{{ job[7] or '' }}</textarea>
        </div>
        
        <div class="form-group">
            <label for="contact_person">联系人</label>
            <input type="text" id="contact_person" name="contact_person" value="{{ job[8] or '' }}">
        </div>
        
        <div class="form-group">
            <label for="contact_phone">联系电话</label>
            <input type="text" id="contact_phone" name="contact_phone" value="{{ job[9] or '' }}">
        </div>
        
        <div class="form-group">
            <label for="email">电子邮箱</label>
            <input type="text" id="email" name="email" value="{{ job[10] or '' }}">
        </div>
        
        <div class="actions">
            <button type="submit" class="btn btn-success">保存更新</button>
            <a href="{{ url_for('view_job', job_id=job[0]) }}" class="btn btn-secondary">取消</a>
        </div>
    </form>
{% endblock %}'''
    
    # 删除岗位模板
    delete_job_html = '''{% extends "base.html" %}
{% block title %}删除岗位 - 岗位管理系统{% endblock %}
{% block content %}
    <h2>确认删除岗位</h2>
    
    <div style="padding: 20px; background-color: #f8d7da; border-radius: 4px; margin-bottom: 20px;">
        <p style="font-weight: bold;">您确定要删除以下岗位吗？</p>
        <p>企业名称: {{ job.company_name }}</p>
        <p>岗位名称: {{ job.job_title }}</p>
        <p>ID: {{ job.id }}</p>
        <p style="color: red; font-weight: bold; margin-top: 15px;">此操作不可撤销！</p>
    </div>
    
    <form action="{{ url_for('delete_job', job_id=job.id) }}" method="post">
        <div class="actions">
            <button type="submit" class="btn btn-danger">确认删除</button>
            <a href="{{ url_for('view_job', job_id=job.id) }}" class="btn btn-secondary">取消</a>
        </div>
    </form>
{% endblock %}'''
    
    # 写入模板文件
    templates = {
        'base.html': base_html,
        'index.html': index_html,
        'add_job.html': add_job_html,
        'view_job.html': view_job_html,
        'update_job.html': update_job_html,
        'delete_job.html': delete_job_html
    }
    
    for filename, content in templates.items():
        with open(os.path.join(templates_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"创建模板文件: {filename}")

# 检查Flask是否安装
def check_flask_installed():
    try:
        import flask
        print(f"检测到Flask已安装，版本: {flask.__version__}")
        return True
    except ImportError:
        return False

# 安装Flask
def install_flask():
    print("正在安装Flask...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
        print("Flask安装成功")
        return True
    except subprocess.CalledProcessError:
        print("Flask安装失败，请手动运行: pip install flask")
        return False

if __name__ == '__main__':
    # 检查并安装Flask
    if not check_flask_installed():
        if not install_flask():
            sys.exit(1)
    
    # 创建模板文件
    create_templates()
    
    print("\n岗位管理系统 - 网页版")
    print("=" * 30)
    print("系统启动中...")
    print("访问地址: http://127.0.0.1:5000/")
    print("按 Ctrl+C 停止服务")
    print("=" * 30)
    
    # 启动Flask应用
    app.run(debug=True, host='0.0.0.0', port=5000)