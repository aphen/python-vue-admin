import request from '@/api/index'
import type { PaginationResponse } from './types/pagination'

export interface Tag {
  id: number
  name: string
  created_by: {
    id: number
    username: string
  }
  created_at: string
  blog_posts_count: number
}

export type TagsResponse = PaginationResponse<Tag>

// 获取标签列表
export const getTags = () => {
  return request<TagsResponse>({
    url: '/polls/api/blog-tags/',
    method: 'get'
  })
}

// 获取热门标签
export const getPopularTags = () => {
  return request<Tag[]>({
    url: '/polls/api/blog-tags/popular/',
    method: 'get'
  })
}

// 创建标签
export const createTag = (data: { name: string }) => {
  return request<Tag>({
    url: '/polls/api/blog-tags/',
    method: 'post',
    data
  })
}

// 删除标签
export const deleteTag = (id: number) => {
  return request({
    url: `/polls/api/blog-tags/${id}/`,
    method: 'delete'
  })
}