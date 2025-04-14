import api from './index'

export interface User {
  id: number
  username: string
  email: string
  date_joined: string
  roles: { id: number; name: string }[]
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