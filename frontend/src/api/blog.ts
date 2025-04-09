import request from '@/api/index'

export interface BlogPost {
  id: number
  title: string
  content: string
  summary: string
  author: {
    id: number
    username: string
  }
  created_at: string
  updated_at: string
}

export interface BlogPostsResponse {
  count: number
  next: string | null
  previous: string | null
  results: BlogPost[]
}

export interface BlogPostsParams {
  page?: number
  page_size?: number
}

// 获取博客文章列表
export const getBlogPosts = (params: BlogPostsParams) => {
  return request<BlogPostsResponse>({
    url: '/api/blog-posts/',
    method: 'get',
    params
  })
}

// 获取博客文章详情
export const getBlogPost = (id: string | number) => {
  return request<BlogPost>({
    url: `/api/blog-posts/${id}/`,
    method: 'get'
  })
}

// 创建博客文章
export const createBlogPost = (data: Partial<BlogPost>) => {
  return request<BlogPost>({
    url: '/api/blog-posts/',
    method: 'post',
    data
  })
}

// 更新博客文章
export const updateBlogPost = (id: number, data: Partial<BlogPost>) => {
  return request<BlogPost>({
    url: `/api/blog-posts/${id}/`,
    method: 'put',
    data
  })
}

// 删除博客文章
export const deleteBlogPost = (id: number) => {
  return request({
    url: `/api/blog-posts/${id}/`,
    method: 'delete'
  })
}