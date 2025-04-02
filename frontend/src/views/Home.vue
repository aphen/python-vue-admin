<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="home-container">
    <h1>欢迎使用投票系统</h1>
    <p>这是一个使用Vue3和Django REST framework构建的前后端分离投票系统。</p>
    <div class="action-buttons">
      <RouterLink to="/polls" class="action-btn">
        开始投票
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

p {
  color: #666;
  margin-bottom: 30px;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.action-btn {
  display: inline-block;
  padding: 12px 24px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.action-btn:hover {
  background-color: #45a049;
}
</style>