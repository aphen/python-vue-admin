// 需要先安装 axios 依赖: npm install axios @types/axios
import axios from 'axios'
import { ElMessageBox } from 'element-plus'
import router from '../router'

// 添加一个全局标志变量，用于跟踪是否已经显示过token过期提醒
let isTokenExpireAlertShown = false

// 导出重置token过期提醒标志的函数，供登录成功后调用
export const resetTokenExpireAlert = () => {
  isTokenExpireAlertShown = false
}

// 创建一个函数来获取CSRF令牌
export const getCsrfToken = async () => {
  try {
    // 发送一个GET请求到Django服务器，这会设置CSRF cookie
    await axios.get('http://localhost:8000/polls/', { withCredentials: true })
    console.log('CSRF token refreshed')
  } catch (error) {
    console.error('Failed to get CSRF token:', error)
  }
}

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    // 如果有token，设置到请求头
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
      // 确保Authorization头被正确设置
      console.log('设置Authorization头:', `Bearer ${token.substring(0, 10)}...`)
    } else {
      console.warn('没有找到access_token，请求将没有认证信息')
    }
    
    // Log request configuration for debugging
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`, {
      hasToken: !!token,
      headers: { ...config.headers, Authorization: token ? 'Bearer [FILTERED]' : undefined }
    })
    
    return config
  },
  error => {
    console.error('Request interceptor error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => {
    // Log successful responses for debugging
    console.log(`API Response [${response.status}]: ${response.config.method?.toUpperCase()} ${response.config.url}`)
    return response
  },
  error => {
    // Log error responses for debugging
    console.error('API Error Response:', {
      url: error.config?.url,
      method: error.config?.method?.toUpperCase(),
      status: error.response?.status,
      data: error.response?.data
    })
    
    // 处理401错误（未授权，token无效或过期）
    if (error.response && error.response.status === 401 && !isTokenExpireAlertShown) {
      // 设置标志为true，防止多次显示
      isTokenExpireAlertShown = true
      
      // 显示token过期提示
      ElMessageBox.confirm(
        'token已过期，将跳转登录页',
        '提示',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning',
          showClose: false,
          closeOnClickModal: false,
          closeOnPressEscape: false
        }
      ).then(() => {
        // 清除token
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        // 跳转到登录页
        return router.push('/login')
      }).catch(() => {
        // 用户取消，不做操作
      }).finally(() => {
        // 无论用户是否确认，都需要在一段时间后重置标志
        // 这样如果用户取消了弹窗但没有登录，一段时间后仍能再次提醒
        setTimeout(() => {
          isTokenExpireAlertShown = false
        }, 60000) // 1分钟后重置
      })
    }
    return Promise.reject(error)
  }
)

// Create a special instance for authentication requests (login/register)
export const authApi = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000,
  withCredentials: true, // 允许跨域请求携带cookie
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

export default api