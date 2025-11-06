#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
岗位管理系统
功能：训练学生使用数据库的增删改查(CRUD)操作
包含：岗位的添加、列表展示、筛选查询、删除和修改功能
"""

import sqlite3
import os
import sys
from datetime import datetime

class JobManagementSystem:
    def __init__(self):
        # 数据库文件名
        self.db_file = 'job_management.db'
        # 连接数据库
        self.conn = None
        self.cursor = None
        self.connect_db()
        self.create_table()
    
    def connect_db(self):
        """连接到SQLite数据库"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            print(f"成功连接到数据库 {self.db_file}")
        except sqlite3.Error as e:
            print(f"数据库连接失败: {e}")
            sys.exit(1)
    
    def create_table(self):
        """创建岗位表"""
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
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            print("岗位表创建成功")
        except sqlite3.Error as e:
            print(f"创建表失败: {e}")
            self.conn.rollback()
    
    def add_job(self):
        """添加新岗位"""
        print("\n=== 添加新岗位 ===")
        
        # 获取用户输入
        company_name = input("企业名称: ").strip()
        if not company_name:
            print("企业名称不能为空")
            return
        
        job_title = input("岗位名称: ").strip()
        if not job_title:
            print("岗位名称不能为空")
            return
        
        salary = input("薪资: ").strip()
        requirements = input("具体要求: ").strip()
        location = input("工作地点: ").strip()
        description = input("岗位描述: ").strip()
        contact_person = input("联系人: ").strip()
        contact_phone = input("联系电话: ").strip()
        email = input("电子邮箱: ").strip()
        
        # 插入数据
        insert_sql = '''
        INSERT INTO jobs (company_name, job_title, salary, requirements, location, 
                         description, contact_person, contact_phone, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        try:
            self.cursor.execute(insert_sql, (
                company_name, job_title, salary, requirements, location,
                description, contact_person, contact_phone, email
            ))
            self.conn.commit()
            print(f"岗位添加成功！ID: {self.cursor.lastrowid}")
        except sqlite3.Error as e:
            print(f"添加岗位失败: {e}")
            self.conn.rollback()
    
    def list_jobs(self, filter_criteria=None):
        """列出岗位，支持筛选"""
        print("\n=== 岗位列表 ===")
        
        # 构建查询SQL
        base_query = """
        SELECT id, company_name, job_title, salary, location, posted_date 
        FROM jobs
        """
        
        if filter_criteria:
            # 根据筛选条件构建WHERE子句
            conditions = []
            params = []
            
            if filter_criteria.get('company_name'):
                conditions.append("company_name LIKE ?")
                params.append(f"%{filter_criteria['company_name']}%")
            
            if filter_criteria.get('job_title'):
                conditions.append("job_title LIKE ?")
                params.append(f"%{filter_criteria['job_title']}%")
            
            if filter_criteria.get('location'):
                conditions.append("location LIKE ?")
                params.append(f"%{filter_criteria['location']}%")
            
            if conditions:
                base_query += " WHERE " + " AND ".join(conditions)
        else:
            params = []
        
        base_query += " ORDER BY posted_date DESC"
        
        try:
            self.cursor.execute(base_query, params)
            jobs = self.cursor.fetchall()
            
            if not jobs:
                print("没有找到岗位记录")
                return []
            
            # 打印表头
            print("-" * 80)
            print(f"{'ID':<5}{'企业名称':<20}{'岗位名称':<20}{'薪资':<10}{'地点':<10}{'发布日期':<10}")
            print("-" * 80)
            
            # 打印岗位列表
            for job in jobs:
                print(f"{job[0]:<5}{job[1]:<20}{job[2]:<20}{job[3] or '':<10}{job[4] or '':<10}{job[5]:<10}")
            
            print("-" * 80)
            print(f"共找到 {len(jobs)} 条记录")
            
            return jobs
        except sqlite3.Error as e:
            print(f"查询岗位失败: {e}")
            return []
    
    def search_jobs(self):
        """搜索岗位"""
        print("\n=== 搜索岗位 ===")
        
        company_name = input("企业名称 (留空跳过): ").strip()
        job_title = input("岗位名称 (留空跳过): ").strip()
        location = input("工作地点 (留空跳过): ").strip()
        
        filter_criteria = {}
        if company_name:
            filter_criteria['company_name'] = company_name
        if job_title:
            filter_criteria['job_title'] = job_title
        if location:
            filter_criteria['location'] = location
        
        return self.list_jobs(filter_criteria)
    
    def view_job_detail(self, job_id):
        """查看岗位详细信息"""
        select_sql = """
        SELECT * FROM jobs WHERE id = ?
        """
        
        try:
            self.cursor.execute(select_sql, (job_id,))
            job = self.cursor.fetchone()
            
            if not job:
                print(f"未找到ID为 {job_id} 的岗位")
                return None
            
            print("\n=== 岗位详细信息 ===")
            print(f"ID: {job[0]}")
            print(f"企业名称: {job[1]}")
            print(f"岗位名称: {job[2]}")
            print(f"薪资: {job[3] or '未填写'}")
            print(f"具体要求: {job[4] or '未填写'}")
            print(f"工作地点: {job[5] or '未填写'}")
            print(f"发布日期: {job[6]}")
            print(f"岗位描述: {job[7] or '未填写'}")
            print(f"联系人: {job[8] or '未填写'}")
            print(f"联系电话: {job[9] or '未填写'}")
            print(f"电子邮箱: {job[10] or '未填写'}")
            
            return job
        except sqlite3.Error as e:
            print(f"查询岗位详情失败: {e}")
            return None
    
    def update_job(self):
        """更新岗位信息"""
        print("\n=== 更新岗位信息 ===")
        
        # 先显示所有岗位
        self.list_jobs()
        
        try:
            job_id = int(input("请输入要更新的岗位ID: ").strip())
        except ValueError:
            print("无效的ID")
            return
        
        # 检查岗位是否存在
        job = self.view_job_detail(job_id)
        if not job:
            return
        
        print("\n请输入更新信息 (留空表示不修改):")
        
        # 获取用户输入，允许留空表示不修改
        company_name = input(f"企业名称 [{job[1]}]: ").strip() or job[1]
        job_title = input(f"岗位名称 [{job[2]}]: ").strip() or job[2]
        salary = input(f"薪资 [{job[3] or '未填写'}]: ").strip() or job[3]
        requirements = input(f"具体要求 [{job[4] or '未填写'}]: ").strip() or job[4]
        location = input(f"工作地点 [{job[5] or '未填写'}]: ").strip() or job[5]
        description = input(f"岗位描述 [{job[7] or '未填写'}]: ").strip() or job[7]
        contact_person = input(f"联系人 [{job[8] or '未填写'}]: ").strip() or job[8]
        contact_phone = input(f"联系电话 [{job[9] or '未填写'}]: ").strip() or job[9]
        email = input(f"电子邮箱 [{job[10] or '未填写'}]: ").strip() or job[10]
        
        # 更新数据
        update_sql = """
        UPDATE jobs SET 
            company_name = ?, job_title = ?, salary = ?, requirements = ?, 
            location = ?, description = ?, contact_person = ?, contact_phone = ?, email = ?
        WHERE id = ?
        """
        
        try:
            self.cursor.execute(update_sql, (
                company_name, job_title, salary, requirements, location,
                description, contact_person, contact_phone, email, job_id
            ))
            self.conn.commit()
            print(f"岗位 {job_id} 更新成功")
        except sqlite3.Error as e:
            print(f"更新岗位失败: {e}")
            self.conn.rollback()
    
    def delete_job(self):
        """删除岗位"""
        print("\n=== 删除岗位 ===")
        
        # 先显示所有岗位
        self.list_jobs()
        
        try:
            job_id = int(input("请输入要删除的岗位ID: ").strip())
        except ValueError:
            print("无效的ID")
            return
        
        # 检查岗位是否存在
        job = self.view_job_detail(job_id)
        if not job:
            return
        
        # 确认删除
        confirm = input(f"确定要删除'{job[1]} - {job[2]}'吗？(y/n): ").strip().lower()
        if confirm != 'y':
            print("已取消删除")
            return
        
        # 删除数据
        delete_sql = "DELETE FROM jobs WHERE id = ?"
        
        try:
            self.cursor.execute(delete_sql, (job_id,))
            self.conn.commit()
            print(f"岗位 {job_id} 删除成功")
        except sqlite3.Error as e:
            print(f"删除岗位失败: {e}")
            self.conn.rollback()
    
    def display_menu(self):
        """显示菜单"""
        print("\n" + "=" * 30)
        print("      岗位管理系统")
        print("=" * 30)
        print("1. 添加新岗位")
        print("2. 查看所有岗位")
        print("3. 搜索岗位")
        print("4. 更新岗位信息")
        print("5. 删除岗位")
        print("6. 退出系统")
        print("=" * 30)
    
    def run(self):
        """运行系统"""
        while True:
            self.display_menu()
            
            choice = input("请选择操作 (1-6): ").strip()
            
            if choice == '1':
                self.add_job()
            elif choice == '2':
                self.list_jobs()
                
                # 询问是否查看详情
                job_id_input = input("\n输入岗位ID查看详情 (留空返回): ").strip()
                if job_id_input:
                    try:
                        job_id = int(job_id_input)
                        self.view_job_detail(job_id)
                    except ValueError:
                        print("无效的ID")
            elif choice == '3':
                results = self.search_jobs()
                
                # 如果有结果，询问是否查看详情
                if results:
                    job_id_input = input("\n输入岗位ID查看详情 (留空返回): ").strip()
                    if job_id_input:
                        try:
                            job_id = int(job_id_input)
                            self.view_job_detail(job_id)
                        except ValueError:
                            print("无效的ID")
            elif choice == '4':
                self.update_job()
            elif choice == '5':
                self.delete_job()
            elif choice == '6':
                print("\n感谢使用岗位管理系统，再见！")
                break
            else:
                print("无效的选择，请重新输入")
            
            input("\n按回车键继续...")
    
    def __del__(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            print("数据库连接已关闭")


def main():
    """主函数"""
    print("欢迎使用岗位管理系统！")
    print("本系统用于训练数据库的增删改查操作")
    
    try:
        system = JobManagementSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"程序发生错误: {e}")
    finally:
        print("程序已退出")


if __name__ == "__main__":
    main()