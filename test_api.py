#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API功能测试脚本
直接在服务器端测试增删改查功能
"""

import requests
import json
import time

BASE_URL = 'http://127.0.0.1:5000/api'

def test_get_jobs():
    """测试获取岗位列表"""
    print("\n1. 测试获取岗位列表")
    try:
        response = requests.get(f"{BASE_URL}/jobs")
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"岗位数量: {len(data.get('data', []))}")
        return True
    except Exception as e:
        print(f"获取岗位列表失败: {str(e)}")
        return False

def test_add_job():
    """测试添加新岗位"""
    print("\n2. 测试添加新岗位")
    try:
        new_job = {
            "company_name": "测试公司",
            "job_title": "测试岗位",
            "salary": "15k-25k",
            "location": "北京",
            "application_date": "2024-01-20",
            "status": "已投递",
            "notes": "这是一条测试记录"
        }
        
        response = requests.post(
            f"{BASE_URL}/jobs",
            headers={"Content-Type": "application/json"},
            json=new_job
        )
        
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if data.get('success') and data.get('id'):
            print(f"成功添加岗位，ID: {data['id']}")
            return data['id']  # 返回新添加的岗位ID
        else:
            print(f"添加岗位失败: {data.get('error', '未知错误')}")
            return None
    except Exception as e:
        print(f"添加岗位失败: {str(e)}")
        return None

def test_update_job(job_id):
    """测试更新岗位"""
    if not job_id:
        print("跳过更新测试：没有有效的岗位ID")
        return False
        
    print(f"\n3. 测试更新岗位 (ID: {job_id})")
    try:
        updated_job = {
            "company_name": "更新后的公司",
            "job_title": "更新后的岗位",
            "salary": "20k-30k",
            "location": "上海",
            "application_date": "2024-01-21",
            "status": "待面试",
            "notes": "这是更新后的测试记录"
        }
        
        response = requests.put(
            f"{BASE_URL}/job/{job_id}",
            headers={"Content-Type": "application/json"},
            json=updated_job
        )
        
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if data.get('success'):
            print("成功更新岗位")
            return True
        else:
            print(f"更新岗位失败: {data.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"更新岗位失败: {str(e)}")
        return False

def test_delete_job(job_id):
    """测试删除岗位"""
    if not job_id:
        print("跳过删除测试：没有有效的岗位ID")
        return False
        
    print(f"\n4. 测试删除岗位 (ID: {job_id})")
    try:
        response = requests.delete(f"{BASE_URL}/job/{job_id}")
        
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if data.get('success'):
            print("成功删除岗位")
            return True
        else:
            print(f"删除岗位失败: {data.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"删除岗位失败: {str(e)}")
        return False

def test_get_single_job(job_id):
    """测试获取单个岗位详情"""
    if not job_id:
        print("跳过获取单个岗位测试：没有有效的岗位ID")
        return False
        
    print(f"\n测试获取单个岗位 (ID: {job_id})")
    try:
        response = requests.get(f"{BASE_URL}/job/{job_id}")
        
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        return data.get('success', False)
    except Exception as e:
        print(f"获取单个岗位失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("开始测试岗位管理系统API功能")
    print("=" * 50)
    
    # 测试获取岗位列表
    test_get_jobs()
    
    # 测试添加岗位
    job_id = test_add_job()
    
    # 短暂延迟，确保数据保存完成
    time.sleep(1)
    
    # 测试获取单个岗位（添加后）
    if job_id:
        test_get_single_job(job_id)
    
    # 测试更新岗位
    update_success = test_update_job(job_id)
    
    # 短暂延迟，确保数据更新完成
    time.sleep(1)
    
    # 测试获取单个岗位（更新后）
    if job_id and update_success:
        test_get_single_job(job_id)
    
    # 测试获取岗位列表（操作后）
    test_get_jobs()
    
    # 测试删除岗位
    test_delete_job(job_id)
    
    # 短暂延迟，确保数据删除完成
    time.sleep(1)
    
    # 测试获取岗位列表（删除后）
    test_get_jobs()
    
    print("\n" + "=" * 50)
    print("API功能测试完成")
    print("=" * 50)

if __name__ == "__main__":
    main()