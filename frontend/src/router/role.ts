import type { RouteRecordRaw } from 'vue-router'

const roleRoutes: RouteRecordRaw[] = [
  {
    path: '/role',
    name: 'RoleManagement',
    component: () => import('@/views/RoleManagement.vue'),
    meta: {
      title: '角色管理',
      requiresAuth: true
    }
  }
]

export default roleRoutes