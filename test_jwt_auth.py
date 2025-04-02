import requests
import json
import sys

# 测试JWT认证流程
print('===== 测试JWT认证流程 =====')

# 服务器基础URL
BASE_URL = 'http://localhost:8000'

# 1. 获取token
def get_token(username, password):
    token_url = f'{BASE_URL}/api/token/'
    login_data = {
        'username': username,
        'password': password
    }
    
    print(f'\n1. 尝试登录用户: {username}')
    try:
        response = requests.post(token_url, json=login_data)
        print(f'状态码: {response.status_code}')
        
        if response.status_code == 200:
            token_data = response.json()
            print('登录成功! 获取到令牌')
            return token_data
        else:
            print('登录失败:')
            print(response.text)
            return None
    except Exception as e:
        print(f'请求出错: {str(e)}')
        return None

# 2. 获取用户信息
def get_user_info(access_token):
    me_url = f'{BASE_URL}/polls/api/users/me/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    print('\n2. 获取用户信息')
    print(f'请求URL: {me_url}')
    print(f'Authorization: Bearer {access_token[:10]}...')
    
    try:
        response = requests.get(me_url, headers=headers)
        print(f'状态码: {response.status_code}')
        
        if response.status_code == 200:
            print('获取用户信息成功:')
            print(json.dumps(response.json(), indent=2))
            return response.json()
        else:
            print('获取用户信息失败:')
            print(response.text)
            return None
    except Exception as e:
        print(f'请求出错: {str(e)}')
        return None

# 主函数
def main():
    # 获取命令行参数
    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
    else:
        username = input('请输入用户名: ')
        password = input('请输入密码: ')
    
    # 1. 获取token
    token_data = get_token(username, password)
    if not token_data:
        print('\n无法继续测试，因为无法获取令牌')
        return
    
    access_token = token_data.get('access')
    refresh_token = token_data.get('refresh')
    
    # 2. 获取用户信息
    user_info = get_user_info(access_token)
    if not user_info:
        print('\n获取用户信息失败')
    
    print('\n===== 测试完成 =====')

if __name__ == '__main__':
    main()