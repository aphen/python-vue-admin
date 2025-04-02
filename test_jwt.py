import requests

# 测试JWT认证
print('测试JWT认证')

# 1. 获取token
token_url = 'http://localhost:8000/api/token/'
login_data = {
    'username': 'admin',  # 替换为有效的用户名
    'password': 'admin'   # 替换为有效的密码
}

try:
    # 获取token
    token_response = requests.post(token_url, json=login_data)
    print(f'Token请求状态码: {token_response.status_code}')
    
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get('access')
        print('成功获取访问令牌')
        
        # 2. 使用token请求me接口
        me_url = 'http://localhost:8000/polls/api/users/me/'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        # 打印完整请求信息
        print(f'\n请求URL: {me_url}')
        print(f'请求头: {headers}')
        
        me_response = requests.get(me_url, headers=headers)
        print(f'\nMe接口请求状态码: {me_response.status_code}')
        
        if me_response.status_code == 200:
            print('成功获取用户信息:')
            print(me_response.json())
        else:
            print('获取用户信息失败:')
            print(me_response.text)
    else:
        print('获取token失败:')
        print(token_response.text)
        
except Exception as e:
    print(f'发生错误: {str(e)}')