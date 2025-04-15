import api from './index'

export interface User {
  id: number
  username: string
  email: string
  date_joined: string
  roles: { id: number; name: string }[]
  is_staff?: boolean
  is_superuser?: boolean
  permissions?: any[]
}

export interface CreateUserData {
  username: string
  email: string
  password: string
}

export interface UserResponse {
  count: number
  results: User[]
}

// 获取当前登录用户信息
export const getCurrentUser = async () => {
  const response = await api.get<User>('/polls/api/users/me/')
  return response.data
}

// 更新当前登录用户信息
export const updateCurrentUser = async (data: Partial<User>) => {
  const response = await api.put<User>('/polls/api/users/me/', data)
  return response.data
}

// 根据角色ID获取权限
export const getPermissionsByRoleIds = async (roleIds: string) => {
  const response = await api.get('/polls/api/roles/permissions_by_role_ids/', {
    params: {
      role_ids: roleIds,
    },
  })
  return response.data
}

// 获取用户列表
export const getUsers = async (page = 1, pageSize = 10) => {
  const response = await api.get<UserResponse>('/polls/api/users/', {
    params: {
      page,
      page_size: pageSize
    }
  })
  return response.data
}

export const createUser = async (data: CreateUserData) => {
  const response = await api.post<User>('/polls/api/users/', data)
  return response.data
}

export const updateUser = async (id: number, data: Partial<User>) => {
  const response = await api.put<User>(`/polls/api/users/${id}/`, data)
  return response.data
}

export const deleteUser = async (id: number) => {
  await api.delete(`/polls/api/users/${id}/`)
}