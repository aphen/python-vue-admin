import api from './index'

/**
 * 获取操作日志列表
 * @param params 查询参数，包括分页、过滤和排序
 * @returns Promise 包含操作日志列表数据
 */
export const getOperationLogs = (params: any) => {
  return api.get('/polls/api/operation-logs/', { params })
}

/**
 * 获取操作日志详情
 * @param id 操作日志ID
 * @returns Promise 包含操作日志详情数据
 */
export const getOperationLogDetail = (id: number) => {
  return api.get(`/polls/api/operation-logs/${id}/`)
}