import request from './index'

export interface Department {
  id: number
  name: string
  parent: number | null
  parent_name?: string
  order: number
  children?: Department[]
}

export interface DepartmentForm {
  id?: number
  name: string
  parent: number | null
  order: number
}

// 获取部门列表
export const getDepartmentList = () => {
  return request.get<Department[]>('/polls/api/departments/')
}

// 创建部门
export const createDepartment = (data: DepartmentForm) => {
  return request.post<Department>('/polls/api/departments/', data)
}

// 更新部门
export const updateDepartment = (id: number, data: DepartmentForm) => {
  return request.put<Department>(`/polls/api/departments/${id}/`, data)
}

// 删除部门
export const deleteDepartment = (id: number) => {
  return request.delete(`/polls/api/departments/${id}/`)
}