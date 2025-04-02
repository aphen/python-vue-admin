<template>
  <div class="register-container">
    <el-card class="register-box">
      <template #header>
        <h2 class="register-title">注册</h2>
      </template>
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        @submit.prevent="handleRegister"
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
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="formData.email"
            :prefix-icon="Message"
            placeholder="请输入邮箱"
            autocomplete="email"
          />
        </el-form-item>
        <el-form-item label="名字" prop="first_name">
          <el-input
            v-model="formData.first_name"
            :prefix-icon="UserFilled"
            placeholder="请输入名字"
          />
        </el-form-item>
        <el-form-item label="姓氏" prop="last_name">
          <el-input
            v-model="formData.last_name"
            :prefix-icon="UserFilled"
            placeholder="请输入姓氏"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="formData.password"
            :prefix-icon="Lock"
            type="password"
            show-password
            placeholder="请输入密码"
            autocomplete="new-password"
          />
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="password2">
          <el-input
            v-model="formData.password2"
            :prefix-icon="Lock"
            type="password"
            show-password
            placeholder="请再次输入密码"
            autocomplete="new-password"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            class="submit-btn"
            @click="handleRegister"
          >
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
          <div class="login-link">
            已有账号？<router-link to="/login">去登录</router-link>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, UserFilled, Lock, Message } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import api from '@/api'

const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)
const formData = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: '',
  password2: ''
})

const validatePass2 = (_rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== formData.value.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = ref<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  first_name: [
    { required: true, message: '请输入名字', trigger: 'blur' },
    { min: 1, max: 30, message: '名字长度应在1-30个字符之间', trigger: 'blur' }
  ],
  last_name: [
    { required: true, message: '请输入姓氏', trigger: 'blur' },
    { min: 1, max: 30, message: '姓氏长度应在1-30个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在6-20个字符之间', trigger: 'blur' }
  ],
  password2: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ]
})

const handleRegister = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true
    await api.post('/polls/api/register/', formData.value)
    ElMessage.success('注册成功！')
    router.push('/login')
  } catch (error: any) {
    console.error('注册失败:', error)
    if (error.response?.data) {
      const errors = Object.entries(error.response.data)
        .map(([key, value]) => `${key}: ${value}`)
        .join('\n')
      ElMessage.error(`注册失败：${errors}`)
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.register-box {
  width: 100%;
  max-width: 420px;
}

.register-title {
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

.login-link {
  text-align: center;
  margin-top: 16px;
  color: var(--el-text-color-regular);
}

.login-link a {
  color: var(--el-color-primary);
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .register-box {
    max-width: 100%;
  }
}

.login-link {
  text-align: center;
  margin-top: 1rem;
}

.login-link a {
  color: #4a90e2;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>