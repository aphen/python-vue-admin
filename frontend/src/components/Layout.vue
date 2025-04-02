<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { User, House, List, Setting } from '@element-plus/icons-vue'

const isCollapse = ref(false)
const router = useRouter()

const handleSelect = (key: string) => {
  router.push(key)
}
</script>

<template>

    <div class="container">
      <el-menu
        class="sidebar"
        :collapse="isCollapse"
        @select="handleSelect"
        :default-active="router.currentRoute.value.path"
        router
      >
        <el-menu-item index="/home">
          <el-icon><House /></el-icon>
          <template #title>首页</template>
        </el-menu-item>
        <el-menu-item index="/polls">
          <el-icon><List /></el-icon>
          <template #title>投票</template>
        </el-menu-item>
        <el-sub-menu index="system">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-sub-menu index="user">
            <template #title>
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </template>
            <el-menu-item index="/user/list">用户列表</el-menu-item>
            <el-menu-item index="/user/profile">个人信息</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/role/list">
            <el-icon><Setting /></el-icon>
            <span>角色管理</span>
          </el-menu-item>
          <el-menu-item index="/department/list">
            <el-icon><Setting /></el-icon>
            <span>部门管理</span>
          </el-menu-item>
          <el-menu-item index="/system/monitor">
            <el-icon><Setting /></el-icon>
            <span>服务监控</span>
          </el-menu-item>
          <el-menu-item index="/system/operation-log">
            <el-icon><Setting /></el-icon>
            <span>操作日志</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
      <div class="main-content">
        <router-view />
      </div>
    </div>

</template>

<style scoped>
.container {
  display: flex;
  height: 100%;
}
.sidebar {
  border-right: solid 1px #e6e6e6;
  height: 100%;
  margin-top: 2px;
  padding-top: 12px;
  overflow-y: auto;
}

.sidebar:not(.el-menu--collapse) {
  width: 200px;
}
.main-content {
  flex: 1;
  height: 100%;
  overflow-y: auto;
  padding: 0 20px;
}

:deep(.el-menu-item.is-active) {
  background-color: var(--el-menu-hover-bg-color);
}

:deep(.el-sub-menu .el-menu-item) {
  min-width: 200px;
}

:deep(.el-menu-item:hover) {
  background-color: var(--el-menu-hover-bg-color);
}
</style>