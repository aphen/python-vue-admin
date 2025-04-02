<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import { logout } from '../api/auth'

const router = useRouter()

// 退出登录
const handleLogout = () => {
  ElMessageBox.confirm(
    '确定要退出登录吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      console.log('Refresh token found:', !!refreshToken)
      
      if (!refreshToken) {
        throw new Error('未找到刷新令牌')
      }
      
      console.log('Access token present:', !!localStorage.getItem('access_token'))
      await logout(refreshToken)
      
      // 显示退出成功提示
      ElMessage.success('退出成功')
      
      // 不需要在这里清除token，因为logout函数已经处理了
      // 跳转到登录页
      router.push('/login')
    } catch (error: any) {
      console.error('退出登录失败:', error)
      // 显示更详细的错误信息
      const errorMessage = error.response?.data?.error || error.message || '退出登录失败，请重试'
      ElMessage.warning(errorMessage)
    }
  }).catch(() => {
    // 用户取消，不做操作
  })
}
</script>

<template>
  <div class="navbar">
    <div class="nav-left">
      <router-link to="/home" class="nav-logo">投票系统</router-link>
      <!-- <div class="nav-links">
        <router-link to="/home" class="nav-link">首页</router-link>
        <router-link to="/polls" class="nav-link">投票</router-link>
      </div> -->
    </div>
    <div class="nav-right">
      <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
    </div>
  </div>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  height: 60px;
  width: calc(100% - 80px);
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-left {
  display: flex;
  align-items: center;
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #409EFF;
  text-decoration: none;
  margin-right: 30px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: #606266;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #409EFF;
}

.nav-right {
  display: flex;
  align-items: center;
}
</style>