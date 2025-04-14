import request from './index'

// 获取角色列表
export const getRoles = () => {
  return request({
    url: '/polls/api/roles/',
    method: 'get'
  })
}

// 创建角色
export const createRole = (data: any) => {
  return request({
    url: '/polls/api/roles/',
    method: 'post',
    data
  })
}

// 更新角色
export const updateRole = (id: number, data: any) => {
  return request({
    url: `/polls/api/roles/${id}/`,
    method: 'put',
    data
  })
}

// 删除角色
export const deleteRole = (id: number) => {
  return request({
    url: `/polls/api/roles/${id}/`,
    method: 'delete'
  })
}

// 分配用户
export const assignUsers = (roleId: number, userIds: number[]) => {
  return request({
    url: `/polls/api/roles/${roleId}/assign_users/`,
    method: 'post',
    data: { user_ids: userIds }
  })
}

// 获取所有权限
export function getPermissions() {
  return request({
    url: '/polls/api/roles/permissions/',
    method: 'get'
  })
}

// 分配权限
export function assignPermissions(roleId: string, permissionIds: string[]) {
  return request({
    url: `/polls/api/roles/${roleId}/assign_permissions/`,
    method: 'post',
    data: { permission_ids: permissionIds }
  })
}