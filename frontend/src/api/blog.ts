import request from '@/api/index'

export interface BlogPost {
  id: number
  title?: string
  content: string
  summary: string
  author: {
    id: number
    username: string
  }
  created_at: string
  updated_at: string
  tags?: string[]
}

import type { PaginationResponse } from './types/pagination'

export type BlogPostsResponse = PaginationResponse<BlogPost>

export interface BlogPostsParams {
  page?: number
  page_size?: number
}

export interface BlogComment {
  id: number
  post: number
  author: {
    id: number
    username: string
  }
  content: string
  created_at: string
  updated_at: string
}

export type BlogCommentsResponse = PaginationResponse<BlogComment>

// 获取博客文章列表
export const getBlogPosts = (params: BlogPostsParams) => {
  return request<BlogPostsResponse>({
    url: '/polls/api/blog-posts/',
    method: 'get',
    params
  })
}

// 获取博客文章详情
export const getBlogPost = (id: string | number) => {
  return request<BlogPost>({
    url: `/polls/api/blog-posts/${id}/`,
    method: 'get'
  })
}

// 创建博客文章
export const createBlogPost = (data: Partial<BlogPost>) => {
  return request<BlogPost>({
    url: '/polls/api/blog-posts/',
    method: 'post',
    data
  })
}

// 更新博客文章
export const updateBlogPost = (id: number, data: Partial<BlogPost>) => {
  return request<BlogPost>({
    url: `/polls/api/blog-posts/${id}/`,
    method: 'put',
    data
  })
}

// 删除博客文章
export const deleteBlogPost = (id: number) => {
  return request({
    url: `/polls/api/blog-posts/${id}/`,
    method: 'delete'
  })
}

// 获取文章评论列表
export const getBlogComments = (postId: string | number) => {
  return request<BlogCommentsResponse>({
    url: '/polls/api/blog-comments/',
    method: 'get',
    params: { post_id: postId }
  })
}

// 创建评论
export const createBlogComment = (data: { post: number; content: string; author_id: number }) => {
  return request<BlogComment>({
    url: '/polls/api/blog-comments/',
    method: 'post',
    data
  })
}

// 删除评论
export const deleteBlogComment = (id: number) => {
  return request({
    url: `/polls/api/blog-comments/${id}/`,
    method: 'delete'
  })
}