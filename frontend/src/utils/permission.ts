import type{ RouteLocationNormalized } from 'vue-router'
import { useUserStore } from '@/store/user'

// 菜单权限映射表
const menuPermissionMap = {
  '/user/list': 'view_user',
  '/user/profile': 'view_profile',
  '/role/list': 'view_role',
  '/department/list': 'view_department',
  '/system/monitor': 'view_monitor',
  '/system/operation-log': 'view_operation_log',
  '/blog/list': 'view_blogpost',
  '/blog/create': 'add_blog',
  '/todo': 'view_todo',
  '/polls': 'view_poll'
}

// 检查用户是否有访问某个路由的权限
export function hasPermission(route: RouteLocationNormalized): boolean {
  const userStore = useUserStore()
  const requiredPermission = menuPermissionMap[route.path as keyof typeof menuPermissionMap]

  // 如果路由不需要权限，或者用户是超级管理员，则允许访问
  if (!requiredPermission || userStore.is_superuser) {
    return true
  }

  // 检查用户是否拥有所需权限
  return userStore.permissions.includes(requiredPermission)
}

// 根据权限过滤菜单项
export function filterMenuItems(menuItems: any[]): any[] {
  const userStore = useUserStore()

  return menuItems.filter(item => {
    // 如果是超级管理员，显示所有菜单
    if (userStore.is_superuser) {
      return true
    }

    // 检查当前菜单项是否需要权限
    const permission = menuPermissionMap[item.path as keyof typeof menuPermissionMap]
    if (!permission) {
      return true // 不需要权限的菜单项显示
    }

    // 检查用户是否拥有权限
    return userStore.permissions.includes(permission)
  })
}