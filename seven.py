#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IT岗位求职记录系统
功能：记录和管理适合自己的IT岗位求职信息
"""

import json
import os
import datetime
import time
from tabulate import tabulate

class JobApplicationSystem:
    def __init__(self, data_file='job_applications.json'):
        """初始化系统"""
        self.data_file = data_file
        self.jobs = []
        self.load_data()
    
    def load_data(self):
        """从文件加载求职记录数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.jobs = json.load(f)
                print(f"成功加载 {len(self.jobs)} 条求职记录")
            else:
                print("未找到数据文件，将创建新的记录系统")
        except Exception as e:
            print(f"加载数据失败: {e}")
            self.jobs = []
    
    def save_data(self):
        """保存求职记录数据到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.jobs, f, ensure_ascii=False, indent=2)
            print("数据保存成功")
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def add_job(self):
        """添加新的求职记录"""
        print("\n=== 添加新的IT岗位求职记录 ===")
        
        company = input("公司名称: ").strip()
        position = input("岗位名称: ").strip()
        salary = input("薪资范围 (如: 15k-25k): ").strip()
        location = input("工作地点: ").strip()
        
        while True:
            try:
                apply_date = input("投递日期 (YYYY-MM-DD, 默认为今天): ").strip()
                if not apply_date:
                    apply_date = datetime.datetime.now().strftime('%Y-%m-%d')
                else:
                    # 验证日期格式
                    datetime.datetime.strptime(apply_date, '%Y-%m-%d')
                break
            except ValueError:
                print("日期格式错误，请使用 YYYY-MM-DD 格式")
        
        description = input("岗位描述摘要: ").strip()
        requirements = input("岗位要求摘要: ").strip()
        
        # 可选信息
        print("\n以下为可选信息，直接回车跳过")
        contact = input("联系人: ").strip()
        phone = input("联系电话: ").strip()
        email = input("联系邮箱: ").strip()
        source = input("招聘来源 (如: 拉勾网、BOSS直聘等): ").strip()
        
        # 状态选项
        status_options = ["已投递", "待面试", "面试中", "已通过", "已拒绝", "已放弃"]
        print(f"\n请选择当前状态: {', '.join([f'{i+1}.{opt}' for i, opt in enumerate(status_options)])}")
        
        while True:
            try:
                status_idx = int(input("请输入序号 (默认1): ").strip() or "1") - 1
                if 0 <= status_idx < len(status_options):
                    status = status_options[status_idx]
                    break
                else:
                    print("输入序号超出范围")
            except ValueError:
                print("请输入有效的数字序号")
        
        notes = input("备注信息: ").strip()
        
        # 创建新记录
        job_id = len(self.jobs) + 1
        new_job = {
            'id': job_id,
            'company': company,
            'position': position,
            'salary': salary,
            'location': location,
            'apply_date': apply_date,
            'description': description,
            'requirements': requirements,
            'contact': contact,
            'phone': phone,
            'email': email,
            'source': source,
            'status': status,
            'notes': notes,
            'update_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.jobs.append(new_job)
        print("\n=== 记录添加成功 ===")
        print(f"记录ID: {job_id}")
        self.save_data()
    
    def display_jobs(self, jobs=None, show_all=False):
        """显示求职记录列表"""
        if jobs is None:
            jobs = self.jobs
        
        if not jobs:
            print("没有找到求职记录")
            return
        
        # 准备表格数据
        headers = ["ID", "公司", "岗位", "薪资", "地点", "投递日期", "状态", "来源"]
        table_data = []
        
        for job in jobs:
            row = [
                job['id'],
                job['company'],
                job['position'],
                job['salary'],
                job['location'],
                job['apply_date'],
                job['status'],
                job['source'] if job['source'] else "-"
            ]
            table_data.append(row)
        
        # 显示表格
        print("\n=== IT岗位求职记录列表 ===")
        print(tabulate(table_data, headers=headers, tablefmt='grid', maxcolwidths=[None, 15, 20, 10, 10, 12, 10, 15]))
        
        # 如果需要查看详细信息
        if not show_all and len(jobs) > 0:
            choice = input("\n是否查看某个记录的详细信息？输入ID或直接回车返回: ").strip()
            if choice:
                try:
                    job_id = int(choice)
                    self.view_job_detail(job_id)
                except ValueError:
                    print("无效的ID")
    
    def view_job_detail(self, job_id):
        """查看单个求职记录的详细信息"""
        job = self._find_job_by_id(job_id)
        if not job:
            print(f"未找到ID为 {job_id} 的记录")
            return
        
        print(f"\n=== 求职记录详情 (ID: {job_id}) ===")
        print(f"公司名称: {job['company']}")
        print(f"岗位名称: {job['position']}")
        print(f"薪资范围: {job['salary']}")
        print(f"工作地点: {job['location']}")
        print(f"投递日期: {job['apply_date']}")
        print(f"岗位描述: {job['description'] if job['description'] else '未填写'}")
        print(f"岗位要求: {job['requirements'] if job['requirements'] else '未填写'}")
        print(f"联系人: {job['contact'] if job['contact'] else '未填写'}")
        print(f"联系电话: {job['phone'] if job['phone'] else '未填写'}")
        print(f"联系邮箱: {job['email'] if job['email'] else '未填写'}")
        print(f"招聘来源: {job['source'] if job['source'] else '未填写'}")
        print(f"当前状态: {job['status']}")
        print(f"备注信息: {job['notes'] if job['notes'] else '未填写'}")
        print(f"更新时间: {job['update_time']}")
    
    def search_jobs(self):
        """搜索求职记录"""
        print("\n=== 搜索求职记录 ===")
        print("搜索条件 (直接回车跳过):")
        
        company = input("公司名称: ").strip().lower()
        position = input("岗位名称: ").strip().lower()
        location = input("工作地点: ").strip().lower()
        
        status_options = ["", "已投递", "待面试", "面试中", "已通过", "已拒绝", "已放弃"]
        print(f"状态筛选: {', '.join([f'{i}.{opt}' for i, opt in enumerate(status_options)])}")
        
        try:
            status_idx = int(input("请输入序号 (默认0，不筛选): ").strip() or "0")
            if 0 <= status_idx < len(status_options):
                status = status_options[status_idx]
            else:
                status = ""
        except ValueError:
            status = ""
        
        # 执行搜索
        results = []
        for job in self.jobs:
            match = True
            
            if company and company not in job['company'].lower():
                match = False
            if position and position not in job['position'].lower():
                match = False
            if location and location not in job['location'].lower():
                match = False
            if status and status != job['status']:
                match = False
            
            if match:
                results.append(job)
        
        print(f"\n找到 {len(results)} 条匹配的记录")
        self.display_jobs(results)
    
    def update_job(self):
        """更新求职记录"""
        if not self.jobs:
            print("没有求职记录可供更新")
            return
        
        self.display_jobs(show_all=True)
        job_id = input("\n请输入要更新的记录ID: ").strip()
        
        try:
            job_id = int(job_id)
            job = self._find_job_by_id(job_id)
            
            if not job:
                print(f"未找到ID为 {job_id} 的记录")
                return
            
            print(f"\n=== 更新记录 (ID: {job_id}) ===")
            print("提示: 直接回车保留原有值")
            
            # 更新字段
            job['company'] = input(f"公司名称 [{job['company']}]: ").strip() or job['company']
            job['position'] = input(f"岗位名称 [{job['position']}]: ").strip() or job['position']
            job['salary'] = input(f"薪资范围 [{job['salary']}]: ").strip() or job['salary']
            job['location'] = input(f"工作地点 [{job['location']}]: ").strip() or job['location']
            
            # 日期验证
            while True:
                apply_date = input(f"投递日期 [{job['apply_date']}]: ").strip() or job['apply_date']
                try:
                    datetime.datetime.strptime(apply_date, '%Y-%m-%d')
                    job['apply_date'] = apply_date
                    break
                except ValueError:
                    print("日期格式错误，请使用 YYYY-MM-DD 格式")
            
            job['description'] = input(f"岗位描述 [{job['description']}]: ").strip() or job['description']
            job['requirements'] = input(f"岗位要求 [{job['requirements']}]: ").strip() or job['requirements']
            job['contact'] = input(f"联系人 [{job['contact']}]: ").strip() or job['contact']
            job['phone'] = input(f"联系电话 [{job['phone']}]: ").strip() or job['phone']
            job['email'] = input(f"联系邮箱 [{job['email']}]: ").strip() or job['email']
            job['source'] = input(f"招聘来源 [{job['source']}]: ").strip() or job['source']
            
            # 更新状态
            status_options = ["已投递", "待面试", "面试中", "已通过", "已拒绝", "已放弃"]
            current_status_idx = status_options.index(job['status']) if job['status'] in status_options else 0
            print(f"状态: {', '.join([f'{i+1}.{opt}' for i, opt in enumerate(status_options)])}")
            
            try:
                status_idx = input(f"请输入序号 [{current_status_idx+1}]: ").strip()
                if status_idx:
                    status_idx = int(status_idx) - 1
                    if 0 <= status_idx < len(status_options):
                        job['status'] = status_options[status_idx]
            except ValueError:
                pass
            
            job['notes'] = input(f"备注信息 [{job['notes']}]: ").strip() or job['notes']
            job['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print("\n=== 记录更新成功 ===")
            self.save_data()
            
        except ValueError:
            print("无效的ID")
    
    def delete_job(self):
        """删除求职记录"""
        if not self.jobs:
            print("没有求职记录可供删除")
            return
        
        self.display_jobs(show_all=True)
        job_id = input("\n请输入要删除的记录ID: ").strip()
        
        try:
            job_id = int(job_id)
            job = self._find_job_by_id(job_id)
            
            if not job:
                print(f"未找到ID为 {job_id} 的记录")
                return
            
            # 确认删除
            confirm = input(f"确定要删除 {job['company']} - {job['position']} 的记录吗？(y/n): ").strip().lower()
            if confirm == 'y':
                self.jobs.remove(job)
                # 重新编号
                for i, j in enumerate(self.jobs, 1):
                    j['id'] = i
                print("\n=== 记录删除成功 ===")
                self.save_data()
            else:
                print("已取消删除操作")
                
        except ValueError:
            print("无效的ID")
    
    def _find_job_by_id(self, job_id):
        """根据ID查找求职记录"""
        for job in self.jobs:
            if job['id'] == job_id:
                return job
        return None
    
    def show_statistics(self):
        """显示求职统计信息"""
        if not self.jobs:
            print("没有求职记录，无法生成统计信息")
            return
        
        print("\n=== 求职记录统计信息 ===")
        print(f"总记录数: {len(self.jobs)}")
        
        # 按状态统计
        status_count = {}
        for job in self.jobs:
            status = job['status']
            status_count[status] = status_count.get(status, 0) + 1
        
        print("\n按状态统计:")
        for status, count in sorted(status_count.items()):
            percentage = (count / len(self.jobs)) * 100
            print(f"{status}: {count} 条 ({percentage:.1f}%)")
        
        # 按地点统计
        location_count = {}
        for job in self.jobs:
            location = job['location']
            location_count[location] = location_count.get(location, 0) + 1
        
        print("\n按地点统计 (前10):")
        sorted_locations = sorted(location_count.items(), key=lambda x: x[1], reverse=True)[:10]
        for location, count in sorted_locations:
            print(f"{location}: {count} 条")
        
        # 按投递日期统计最近的投递
        recent_jobs = sorted(self.jobs, key=lambda x: x['apply_date'], reverse=True)[:5]
        if recent_jobs:
            print("\n最近的5条投递:")
            for job in recent_jobs:
                print(f"{job['apply_date']}: {job['company']} - {job['position']}")
    
    def export_to_csv(self):
        """导出求职记录到CSV文件"""
        if not self.jobs:
            print("没有求职记录可导出")
            return
        
        try:
            csv_file = f"job_applications_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
                # 写入表头
                headers = ["ID", "公司", "岗位", "薪资", "地点", "投递日期", "状态", "来源", "更新时间"]
                f.write(",".join([f'"{h}"' for h in headers]) + "\n")
                
                # 写入数据
                for job in self.jobs:
                    row = [
                        str(job['id']),
                        job['company'],
                        job['position'],
                        job['salary'],
                        job['location'],
                        job['apply_date'],
                        job['status'],
                        job['source'] if job['source'] else "",
                        job['update_time']
                    ]
                    f.write(",".join([f'"{cell.replace("\"", "\"\"")}"' for cell in row]) + "\n")
            
            print(f"成功导出 {len(self.jobs)} 条记录到文件: {csv_file}")
        except Exception as e:
            print(f"导出失败: {e}")
    
    def run(self):
        """运行系统主界面"""
        while True:
            self._clear_screen()
            print("=" * 50)
            print("        IT岗位求职记录系统        ")
            print("=" * 50)
            print("1. 添加新的求职记录")
            print("2. 查看所有求职记录")
            print("3. 搜索求职记录")
            print("4. 更新求职记录")
            print("5. 删除求职记录")
            print("6. 查看统计信息")
            print("7. 导出为CSV文件")
            print("0. 退出系统")
            print("=" * 50)
            
            choice = input("请输入操作编号: ").strip()
            
            if choice == '1':
                self.add_job()
            elif choice == '2':
                self.display_jobs()
            elif choice == '3':
                self.search_jobs()
            elif choice == '4':
                self.update_job()
            elif choice == '5':
                self.delete_job()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                self.export_to_csv()
            elif choice == '0':
                print("\n感谢使用IT岗位求职记录系统，再见！")
                time.sleep(1)
                break
            else:
                print("\n无效的操作编号，请重新输入")
            
            if choice != '0':
                input("\n按回车键继续...")
    
    def _clear_screen(self):
        """清屏函数"""
        os.system('cls' if os.name == 'nt' else 'clear')

def check_and_install_dependencies():
    """检查并安装依赖包"""
    try:
        import tabulate
        print("依赖包 'tabulate' 已安装")
    except ImportError:
        print("正在安装依赖包 'tabulate'...")
        try:
            import subprocess
            subprocess.check_call(["pip", "install", "tabulate"])
            print("依赖包安装成功")
        except Exception as e:
            print(f"安装依赖包失败: {e}")
            print("您可以手动安装: pip install tabulate")
            print("或者继续使用，但表格显示功能将不可用")

def main():
    """主函数"""
    print("正在初始化IT岗位求职记录系统...")
    
    # 检查依赖
    check_and_install_dependencies()
    
    # 初始化系统
    system = JobApplicationSystem()
    
    # 运行系统
    system.run()

if __name__ == "__main__":
    main()