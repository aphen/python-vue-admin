<script setup lang="ts">
import NavBar from './components/NavBar.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from './api'
import { useUserStore } from './store/user'

const isLoggedIn = ref(false)
const router = useRouter()
const userStore = useUserStore()

// 检查用户是否登录
const checkLoginStatus = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    isLoggedIn.value = false
    return
  }
  
  try {
    // 初始化用户信息，包括管理员状态
    await userStore.initUserInfo()
    isLoggedIn.value = true
  } catch (error) {
    console.error('Token验证失败:', error)
    isLoggedIn.value = false
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push('/login')
  }
}

onMounted(() => {
  checkLoginStatus()
})
</script>

<template>
  <div class="app-container">
    <NavBar v-if="isLoggedIn && $route.path !== '/login'" />
    <div class="content-container">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
}
.content-container {
  overflow: hidden;
  height: calc(100vh - 60px);
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
