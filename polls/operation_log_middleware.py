from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from .operation_log_models import OperationLog
import json
from django.urls import resolve

class OperationLogMiddleware(MiddlewareMixin):
    """
    操作日志中间件，用于自动记录用户的操作
    """
    def __init__(self, get_response=None):
        self.get_response = get_response
        # 添加async_mode属性，用于支持Django 5.1.7的异步中间件处理
        self.async_mode = False
        # 不需要记录日志的路径
        self.exclude_paths = [
            '/polls/api/system-monitor/',
            '/polls/api/operation-logs/',
        ]
        # 需要记录的请求方法和对应的操作类型
        self.method_operation_map = {
            'POST': 'CREATE',
            'PUT': 'UPDATE',
            'PATCH': 'UPDATE',
            'DELETE': 'DELETE',
        }

    def process_request(self, request):
        # 保存请求体，因为在process_response中可能无法访问
        if request.method in self.method_operation_map and hasattr(request, 'body'):
            request._body = request.body
        return None

    def process_response(self, request, response):
        # 检查是否需要记录日志
        path = request.path
        method = request.method
        
        # 排除不需要记录的路径
        if any(path.startswith(exclude_path) for exclude_path in self.exclude_paths):
            return response
        
        # 只记录特定方法的请求
        if method not in self.method_operation_map:
            return response
        
        # 检查响应状态码，只记录成功的请求
        if not (200 <= response.status_code < 300):
            return response
        
        # 获取用户信息
        user = request.user if request.user.is_authenticated else None
        
        # 获取操作类型
        operation_type = self.method_operation_map.get(method, 'OTHER')
        
        # 获取操作模型
        try:
            url_name = resolve(request.path_info).url_name
            if url_name:
                operation_model = url_name.split('-')[0].capitalize()
            else:
                operation_model = path.split('/')[-2].capitalize()
        except Exception:
            operation_model = path.split('/')[-2].capitalize()
        
        # 获取操作详情
        operation_detail = ''
        if hasattr(request, '_body'):
            try:
                body_data = json.loads(request._body.decode('utf-8'))
                operation_detail = json.dumps(body_data, ensure_ascii=False)
            except Exception:
                operation_detail = str(request._body)
        
        # 获取IP地址
        ip_address = self.get_client_ip(request)
        
        # 记录登录和登出操作
        if path.endswith('/token/') and method == 'POST':
            operation_type = 'LOGIN'
            operation_model = 'User'
        elif path.endswith('/logout/') and method == 'POST':
            operation_type = 'LOGOUT'
            operation_model = 'User'
        
        # 获取请求方法
        request_method = request.method
        
        # 获取请求地址
        request_path = request.path
        
        # 获取用户浏览器信息
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # 获取响应码
        response_code = response.status_code
        
        # 创建操作日志
        OperationLog.objects.create(
            user=user,
            operation_type=operation_type,
            operation_model=operation_model,
            request_path=request_path,
            request_method=request_method,
            user_agent=user_agent,
            response_code=response_code,
            ip_address=ip_address
        )
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip