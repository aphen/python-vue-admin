#!/usr/bin/env python
"""
数据库迁移脚本 - 从SQLite迁移到MySQL

此脚本用于将SQLite数据库中的数据迁移到MySQL数据库。
它会连接两个数据库，并使用Django的ORM API来复制所有数据。
"""

import os
import sys
import django
from pathlib import Path

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# 导入Django模型
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from polls.models import Question, Choice
from polls.role_models import Role
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

# 导入数据库路由器
from django.db import connections

# 定义数据库配置
SQLITE_DB = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': Path(__file__).resolve().parent / 'db.sqlite3',
    'TIME_ZONE': 'UTC',
    'USE_TZ': True,
    'CONN_HEALTH_CHECKS': True,
    'CONN_MAX_AGE': 0,
    'AUTOCOMMIT': True,
    'OPTIONS': {
        'timeout': 20,
    }
}

# 添加SQLite数据库连接
from django.db import connection

# 确保默认数据库连接已关闭
if connection.connection is not None:
    connection.close()

# 添加SQLite数据库连接
connections.databases['sqlite'] = SQLITE_DB

# 确保SQLite数据库连接可用
with connections['sqlite'].cursor() as cursor:
    cursor.execute('SELECT 1')
    cursor.fetchone()

def migrate_users():
    """迁移用户数据"""
    print("开始迁移用户数据...")
    # 从SQLite获取所有用户
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined FROM auth_user")
        users = cursor.fetchall()
    
    # 清空目标数据库中的用户表（除了超级用户）
    User.objects.exclude(is_superuser=True).delete()
    
    # 迁移用户数据
    for user in users:
        # 检查用户是否已存在
        if not User.objects.filter(username=user[4]).exists():
            User.objects.create(
                id=user[0],
                password=user[1],
                last_login=user[2],
                is_superuser=bool(user[3]),
                username=user[4],
                first_name=user[5],
                last_name=user[6],
                email=user[7],
                is_staff=bool(user[8]),
                is_active=bool(user[9]),
                date_joined=user[10]
            )
    print(f"用户数据迁移完成，共迁移 {len(users)} 条记录")

def migrate_groups():
    """迁移用户组数据"""
    print("开始迁移用户组数据...")
    # 从SQLite获取所有用户组
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, name FROM auth_group")
        groups = cursor.fetchall()
    
    # 清空目标数据库中的用户组表
    Group.objects.all().delete()
    
    # 迁移用户组数据
    for group in groups:
        Group.objects.create(
            id=group[0],
            name=group[1]
        )
    print(f"用户组数据迁移完成，共迁移 {len(groups)} 条记录")

def migrate_permissions():
    """迁移权限数据"""
    print("开始迁移权限数据...")
    # 从SQLite获取所有权限
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, name, content_type_id, codename FROM auth_permission")
        permissions = cursor.fetchall()
    
    # 清空目标数据库中的权限表
    Permission.objects.all().delete()
    
    # 迁移权限数据
    for perm in permissions:
        # 确保content_type存在
        if ContentType.objects.filter(id=perm[2]).exists():
            Permission.objects.create(
                id=perm[0],
                name=perm[1],
                content_type_id=perm[2],
                codename=perm[3]
            )
    print(f"权限数据迁移完成，共迁移 {len(permissions)} 条记录")

def migrate_user_groups():
    """迁移用户-组关系数据"""
    print("开始迁移用户-组关系数据...")
    # 从SQLite获取所有用户-组关系
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, user_id, group_id FROM auth_user_groups")
        user_groups = cursor.fetchall()
    
    # 迁移用户-组关系数据
    for ug in user_groups:
        # 确保用户和组都存在
        if User.objects.filter(id=ug[1]).exists() and Group.objects.filter(id=ug[2]).exists():
            user = User.objects.get(id=ug[1])
            group = Group.objects.get(id=ug[2])
            user.groups.add(group)
    print(f"用户-组关系数据迁移完成，共迁移 {len(user_groups)} 条记录")

def migrate_user_permissions():
    """迁移用户-权限关系数据"""
    print("开始迁移用户-权限关系数据...")
    # 从SQLite获取所有用户-权限关系
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, user_id, permission_id FROM auth_user_user_permissions")
        user_permissions = cursor.fetchall()
    
    # 迁移用户-权限关系数据
    for up in user_permissions:
        # 确保用户和权限都存在
        if User.objects.filter(id=up[1]).exists() and Permission.objects.filter(id=up[2]).exists():
            user = User.objects.get(id=up[1])
            permission = Permission.objects.get(id=up[2])
            user.user_permissions.add(permission)
    print(f"用户-权限关系数据迁移完成，共迁移 {len(user_permissions)} 条记录")

def migrate_questions():
    """迁移问题数据"""
    print("开始迁移问题数据...")
    # 从SQLite获取所有问题
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, question_text, pub_date FROM polls_question")
        questions = cursor.fetchall()
    
    # 清空目标数据库中的问题表
    Question.objects.all().delete()
    
    # 迁移问题数据
    for q in questions:
        Question.objects.create(
            id=q[0],
            question_text=q[1],
            pub_date=q[2]
        )
    print(f"问题数据迁移完成，共迁移 {len(questions)} 条记录")

def migrate_choices():
    """迁移选项数据"""
    print("开始迁移选项数据...")
    # 从SQLite获取所有选项
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, question_id, choice_text, votes FROM polls_choice")
        choices = cursor.fetchall()
    
    # 清空目标数据库中的选项表
    Choice.objects.all().delete()
    
    # 迁移选项数据
    for c in choices:
        # 确保问题存在
        if Question.objects.filter(id=c[1]).exists():
            Choice.objects.create(
                id=c[0],
                question_id=c[1],
                choice_text=c[2],
                votes=c[3]
            )
    print(f"选项数据迁移完成，共迁移 {len(choices)} 条记录")

def migrate_roles():
    """迁移角色数据"""
    print("开始迁移角色数据...")
    # 从SQLite获取所有角色
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, name, description, created_at, updated_at FROM polls_role")
        roles = cursor.fetchall()
    
    # 清空目标数据库中的角色表
    Role.objects.all().delete()
    
    # 迁移角色数据
    for r in roles:
        Role.objects.create(
            id=r[0],
            name=r[1],
            description=r[2],
            created_at=r[3],
            updated_at=r[4]
        )
    print(f"角色数据迁移完成，共迁移 {len(roles)} 条记录")

def migrate_role_users():
    """迁移角色-用户关系数据"""
    print("开始迁移角色-用户关系数据...")
    # 从SQLite获取所有角色-用户关系
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, role_id, user_id FROM polls_role_users")
        role_users = cursor.fetchall()
    
    # 迁移角色-用户关系数据
    for ru in role_users:
        # 确保角色和用户都存在
        if Role.objects.filter(id=ru[1]).exists() and User.objects.filter(id=ru[2]).exists():
            role = Role.objects.get(id=ru[1])
            user = User.objects.get(id=ru[2])
            role.users.add(user)
    print(f"角色-用户关系数据迁移完成，共迁移 {len(role_users)} 条记录")

def migrate_tokens():
    """迁移令牌数据"""
    print("开始迁移令牌数据...")
    # 从SQLite获取所有未过期的令牌
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, user_id, jti, token, created_at, expires_at FROM token_blacklist_outstandingtoken")
        tokens = cursor.fetchall()
    
    # 清空目标数据库中的令牌表
    OutstandingToken.objects.all().delete()
    
    # 迁移令牌数据
    for t in tokens:
        # 确保用户存在
        if User.objects.filter(id=t[1]).exists():
            OutstandingToken.objects.create(
                id=t[0],
                user_id=t[1],
                jti=t[2],
                token=t[3],
                created_at=t[4],
                expires_at=t[5]
            )
    print(f"令牌数据迁移完成，共迁移 {len(tokens)} 条记录")

def migrate_blacklisted_tokens():
    """迁移黑名单令牌数据"""
    print("开始迁移黑名单令牌数据...")
    # 从SQLite获取所有黑名单令牌
    with connections['sqlite'].cursor() as cursor:
        cursor.execute("SELECT id, token_id, blacklisted_at FROM token_blacklist_blacklistedtoken")
        blacklisted_tokens = cursor.fetchall()
    
    # 清空目标数据库中的黑名单令牌表
    BlacklistedToken.objects.all().delete()
    
    # 迁移黑名单令牌数据
    for bt in blacklisted_tokens:
        # 确保令牌存在
        if OutstandingToken.objects.filter(id=bt[1]).exists():
            BlacklistedToken.objects.create(
                id=bt[0],
                token_id=bt[1],
                blacklisted_at=bt[2]
            )
    print(f"黑名单令牌数据迁移完成，共迁移 {len(blacklisted_tokens)} 条记录")

def main():
    """主函数，执行所有迁移操作"""
    print("开始数据迁移过程...")
    
    # 按照依赖关系顺序执行迁移
    migrate_users()
    migrate_groups()
    migrate_permissions()
    migrate_user_groups()
    migrate_user_permissions()
    migrate_questions()
    migrate_choices()
    migrate_roles()
    migrate_role_users()
    migrate_tokens()
    migrate_blacklisted_tokens()
    
    print("数据迁移完成！")

if __name__ == "__main__":
    main()