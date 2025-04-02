import axios from 'axios'
import request from './index'

// Login function that directly uses axios (not the configured instance)
export const login = async (username: string, password: string) => {
  try {
    console.log('Login attempt for user:', username)
    
    // Create a specific instance for this request to avoid any authentication issues
    const response = await axios({
      method: 'post',
      url: 'http://localhost:8000/api/token/',
      data: { username, password },
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      // Don't send cookies or other credentials
      withCredentials: false
    })
    
    console.log('Login successful')
    return response.data
  } catch (error: any) {
    console.error('Login failed:', error)
    
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Response status:', error.response.status)
      console.error('Response data:', error.response.data)
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received:', error.request)
    } else {
      // Something happened in setting up the request
      console.error('Error setting up request:', error.message)
    }
    
    throw error
  }
}

export const logout = async (refreshToken: string) => {
  try {
    const accessToken = localStorage.getItem('access_token') 
    if (!accessToken) {
      throw new Error('No access token found')
    }
    let response = await request({
      url: '/polls/api/logout/', 
      method: 'post',
      data: { refresh_token: refreshToken }
    })
    // Clear tokens from localStorage after successful logout
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    
    return response.data
  } catch (error) {
    console.error('退出登录失败:', error)
    if (axios.isAxiosError(error)) {
      // 打印更详细的错误信息
      console.error('完整错误信息:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        headers: error.response?.headers,
        config: {
          url: error.config?.url,
          method: error.config?.method,
          headers: error.config?.headers
        }
      })
      
      // If token is invalid or expired, still clear local storage
      if (error.response?.status === 401 || error.response?.status === 403) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    }
    throw error
  }
}