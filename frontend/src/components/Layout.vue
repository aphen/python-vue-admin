<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { User, House, List, Setting, Calendar, Document } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { hasPermission } from '@/utils/permission'

const isCollapse = ref(false)
const router = useRouter()
const userStore = useUserStore()

const handleSelect = (key: string) => {
  router.push(key)
}

// 检查菜单项是否有权限显示
const checkMenuPermission = (path: string) => {
  return hasPermission({ path } as any)
}

// 计算有权限显示的菜单项
const showUserManagement = computed(() => checkMenuPermission('/user/list'))
const showRoleManagement = computed(() => checkMenuPermission('/role/list'))
const showDepartmentManagement = computed(() => checkMenuPermission('/department/list'))
const showSystemMonitor = computed(() => checkMenuPermission('/system/monitor'))
const showOperationLog = computed(() => checkMenuPermission('/system/operation-log'))
const showBlogManagement = computed(() => checkMenuPermission('/blog/list') || checkMenuPermission('/blog/create'))
const showTodo = computed(() => checkMenuPermission('/todo'))
const showPolls = computed(() => checkMenuPermission('/polls'))
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
          <template #title>首页{{showPolls}}</template>
        </el-menu-item>
        <el-menu-item v-if="showPolls" index="/polls">
          <el-icon><List /></el-icon>
          <template #title>投票</template>
        </el-menu-item>
        <el-menu-item v-if="showTodo" index="/todo">
          <el-icon><Calendar /></el-icon>
          <template #title>待办事项</template>
        </el-menu-item>
        <el-sub-menu v-if="showBlogManagement" index="blog">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>博客管理</span>
          </template>
          <el-menu-item v-if="checkMenuPermission('/blog/list')" index="/blog/list">博客列表</el-menu-item>
          <el-menu-item v-if="checkMenuPermission('/blog/create')" index="/blog/create">发布文章</el-menu-item>
        </el-sub-menu>
        <el-sub-menu v-if="showUserManagement || showRoleManagement || showDepartmentManagement || showSystemMonitor || showOperationLog" index="system">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-sub-menu v-if="showUserManagement" index="user">
            <template #title>
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </template>
            <el-menu-item v-if="checkMenuPermission('/user/list')" index="/user/list">用户列表</el-menu-item>
            <el-menu-item v-if="checkMenuPermission('/user/profile')" index="/user/profile">个人信息</el-menu-item>
          </el-sub-menu>
          <el-menu-item v-if="showRoleManagement" index="/role/list">
            <el-icon><Setting /></el-icon>
            <span>角色管理</span>
          </el-menu-item>
          <el-menu-item v-if="showDepartmentManagement" index="/department/list">
            <el-icon><Setting /></el-icon>
            <span>部门管理</span>
          </el-menu-item>
          <el-menu-item v-if="showSystemMonitor" index="/system/monitor">
            <el-icon><Setting /></el-icon>
            <span>服务监控</span>
          </el-menu-item>
          <el-menu-item v-if="showOperationLog" index="/system/operation-log">
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