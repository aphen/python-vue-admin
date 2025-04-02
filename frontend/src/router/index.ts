import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../components/Layout.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: 'home',
          name: 'home',
          component: () => import('../views/Home.vue')
        },
        {
          path: 'polls',
          name: 'polls',
          component: () => import('../views/Polls.vue')
        },
        {
          path: 'user/list',
          name: 'userList',
          component: () => import('../views/user/UserList.vue')
        },
        {
          path: 'user/profile',
          name: 'userProfile',
          component: () => import('../views/user/UserProfile.vue')
        },
        {
          path: 'role/list',
          name: 'roleList',
          component: () => import('../views/RoleManagement.vue')
        },
        {
          path: 'department/list',
          name: 'departmentList',
          component: () => import('../views/DepartmentManagement.vue')
        },
        {
          path: 'system/monitor',
          name: 'systemMonitor',
          component: () => import('../views/SystemMonitor.vue')
        },
        {
          path: 'system/operation-log',
          name: 'operationLog',
          component: () => import('../views/OperationLogManagement.vue')
        }
      ]
    }
  ]
})

export default router