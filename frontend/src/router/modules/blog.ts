import type { RouteRecordRaw } from 'vue-router'

const blogRoutes: RouteRecordRaw = {
  path: '/blog',
  name: 'Blog',
   component: () => import('@/components/Layout.vue'),
  meta: {
    title: '博客管理',
    icon: 'Document'
  },
  children: [
    {
      path: 'list',
      name: 'BlogList',
      component: () => import('@/views/blog/BlogList.vue'),
      meta: {
        title: '博客首页',
        icon: 'List'
      }
    },
    {
      path: 'create',
      name: 'BlogCreate',
      component: () => import('@/views/blog/BlogCreate.vue'),
      meta: {
        title: '发布文章',
        icon: 'Edit'
      }
    },
    {
      path: 'detail/:id',
      name: 'BlogDetail',
      component: () => import('@/views/blog/BlogDetail.vue'),
      meta: {
        title: '文章详情',
        hidden: true
      }
    }
  ]
}

export default blogRoutes