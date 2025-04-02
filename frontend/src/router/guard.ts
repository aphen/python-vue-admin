import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import axios from 'axios'

export function setupRouterGuard(router: any) {
  router.beforeEach((to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    // 不需要登录的路由
    const publicPages = ['/login', '/register']
    const authRequired = !publicPages.includes(to.path)

    // 从localStorage获取token
    const token = localStorage.getItem('access_token')

    // 如果需要登录但没有token，重定向到登录页
    if (authRequired && !token) {
      next('/login')
      return
    }

    // 如果有token，设置到axios请求头
    if (token) {
      // 不仅设置全局axios的默认头，还要确保我们的api实例也有正确的头
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      // 注意：api实例的headers会在api/index.ts的请求拦截器中设置
      console.log('路由守卫: 设置Authorization头')
    }

    next()
  })
}