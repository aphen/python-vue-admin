<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'
import api from '@/api'

const userStore = useUserStore()
const userProfile = ref({
  username: userStore.username,
  email: userStore.email,
  date_joined: userStore.date_joined
})

const handleSubmit = async () => {
  try {
    await api.put('/polls/api/users/me/', {
      email: userProfile.value.email
    })
    userStore.setUserInfo({
      email: userProfile.value.email
    })
    ElMessage.success('个人信息更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error('更新失败，请稍后重试')
  }
}

onMounted(async () => {
  try {
    // 检查是否有token
    const token = localStorage.getItem('access_token')
    if (!token) {
      console.error('获取用户信息失败: 没有找到access_token')
      ElMessage.error('未登录，请先登录')
      return
    }
    
    // 确保请求头中包含token
    console.log('UserProfile: 发送请求前检查Authorization头')
    const headers = api.defaults.headers.common['Authorization']
    console.log('当前Authorization头:', headers ? '已设置' : '未设置')
    
    // 如果没有设置，手动设置一次
    if (!headers) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      console.log('UserProfile: 手动设置Authorization头')
    }
    
    const response = await api.get('/polls/api/users/me/')
    console.log('获取用户信息成功:', response.status)
    userStore.setUserInfo({
      ...response.data,
      isAuthenticated: true
    })
    userProfile.value = {
      username: userStore.username,
      email: userStore.email,
      date_joined: userStore.date_joined
    }
  } catch (error: any) {
    console.error('获取用户信息失败:', error)
    
    // 打印更详细的错误信息
    if (error.response) {
      console.error('错误状态码:', error.response.status)
      console.error('错误详情:', error.response.data)
    }
    
    ElMessage.error('获取用户信息失败')
  }
})
</script>

<template>
  <div class="user-profile">
    <h2>个人信息</h2>
    <el-form :model="userProfile" label-width="100px">
      <el-form-item label="用户名">
        <el-input v-model="userProfile.username" disabled />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="userProfile.email" />
      </el-form-item>
      <el-form-item label="注册时间">
        <el-input v-model="userProfile.date_joined" disabled />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.user-profile {
  max-width: 600px;
}
</style>