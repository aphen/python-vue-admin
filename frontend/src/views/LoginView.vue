<template>
  <div class="login-container">
    <el-card class="login-box">
      <template #header>
        <h2 class="login-title">登录</h2>
      </template>
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        @submit.prevent="handleLogin"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="formData.username"
            :prefix-icon="User"
            placeholder="请输入用户名"
            autocomplete="username"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="formData.password"
            :prefix-icon="Lock"
            type="password"
            placeholder="请输入密码"
            show-password
            autocomplete="current-password"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            class="submit-btn"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import api, { resetTokenExpireAlert } from '@/api'
import { login } from '@/api/auth'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const formData = ref({
  username: '',
  password: ''
})

const rules = ref<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ]
})

const handleLogin = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    console.log('Starting login process for:', formData.value.username)
    
    try {
      // Use our dedicated login function
      const tokenData = await login(formData.value.username, formData.value.password)
      
      // 保存token到localStorage
      localStorage.setItem('access_token', tokenData.access)
      localStorage.setItem('refresh_token', tokenData.refresh)

      // 设置api实例默认headers
      api.defaults.headers.common['Authorization'] = `Bearer ${tokenData.access}`
      
      // 确保Authorization头被正确设置
      console.log('登录成功: 设置Authorization头', `Bearer ${tokenData.access.substring(0, 10)}...`)
      console.log('Tokens saved, fetching user data')
      
      try {
        // 获取用户信息
        const userResponse = await api.get('/polls/api/users/me/')
        userStore.setUserInfo({
          ...userResponse.data,
          isAuthenticated: true
        })

        // 重置token过期提醒标志
        resetTokenExpireAlert()
        
        ElMessage.success('登录成功！')
        // 登录成功后跳转到首页
        router.push('/')
      } catch (userError) {
        console.error('Failed to get user info, but login was successful:', userError)
        // We still proceed with login even if user info fails
        localStorage.setItem('userInfo', JSON.stringify({
          username: formData.value.username,
          isAuthenticated: true
        }))
        ElMessage.warning('登录成功，但无法获取用户详细信息')
        router.push('/')
      }
    } catch (error: any) {
      console.error('Login API error:', error)
      
      if (error.response) {
        console.error('Response status:', error.response.status)
        console.error('Response data:', error.response.data)
        
        // If we have a specific error message from the server, display it
        const errorMessage = error.response.data?.detail || 
                             error.response.data?.error || 
                             '登录失败，请检查用户名和密码'
        ElMessage.error(errorMessage)
      } else if (error.request) {
        console.error('No response received:', error.request)
        ElMessage.error('服务器无响应，请稍后重试')
      } else {
        console.error('Error setting up request:', error.message)
        ElMessage.error('请求错误，请稍后重试')
      }
    }
  } catch (validationError) {
    console.error('Form validation error:', validationError)
    ElMessage.error('请正确填写登录信息')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  /* min-height: 100vh;
  background-color: #f5f7fa; */
  width: 100%;
  padding: 20px;
}

.login-box {
  width: 100%;
  max-width: 420px;
}

.login-title {
  margin: 0;
  font-size: 24px;
  color: var(--el-text-color-primary);
  text-align: center;
}

:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

:deep(.el-card__body) {
  padding: 24px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px var(--el-border-color) inset;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--el-border-color-hover) inset;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset;
}

.submit-btn {
  width: 100%;
  margin-top: 12px;
}

@media (max-width: 480px) {
  .login-box {
    max-width: 100%;
  }
}
</style>