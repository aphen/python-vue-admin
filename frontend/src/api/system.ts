import api from './index'

/**
 * 获取系统资源使用情况
 * @returns Promise 包含CPU、内存和硬盘使用率的数据
 */
export const getSystemResources = () => {
  return api.get('/polls/api/system-monitor/')
}