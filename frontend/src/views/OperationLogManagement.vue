<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { getOperationLogs } from '../api/operation-log'
import { ElMessage } from 'element-plus'
import type { TableColumnCtx } from 'element-plus/es/components/table/src/table-column/defaults'

interface OperationLog {
  id: number
  user: {
    id: number
    username: string
  }
  operation_type: string
  operation_type_display: string
  operation_model: string
  request_path: string
  request_method: string
  user_agent: string
  response_code: number
  ip_address: string
  operation_time: string
}

interface QueryParams {
  page: number
  page_size: number
  operation_type?: string
  operation_model?: string
  user?: number
  search?: string
  ordering?: string
}

const tableData = ref<OperationLog[]>([])
const loading = ref(false)
const total = ref(0)

const queryParams = reactive<QueryParams>({
  page: 1,
  page_size: 10,
  ordering: '-operation_time'
})

const operationTypeOptions = [
  { value: 'CREATE', label: '创建' },
  { value: 'UPDATE', label: '更新' },
  { value: 'DELETE', label: '删除' },
  { value: 'LOGIN', label: '登录' },
  { value: 'LOGOUT', label: '登出' },
  { value: 'OTHER', label: '其他' }
]

// 获取操作日志列表
const fetchOperationLogs = async () => {
  loading.value = true
  try {
    const response = await getOperationLogs({
      page: queryParams.page,
      page_size: queryParams.page_size,
      operation_type: queryParams.operation_type,
      operation_model: queryParams.operation_model,
      user: queryParams.user,
      search: queryParams.search,
      ordering: queryParams.ordering
    })
    tableData.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取操作日志失败:', error)
    ElMessage.error('获取操作日志失败')
  } finally {
    loading.value = false
  }
}

// 处理页码变化
const handleCurrentChange = (val: number) => {
  queryParams.page = val
  fetchOperationLogs()
}

// 处理每页条数变化
const handleSizeChange = (val: number) => {
  queryParams.page_size = val
  queryParams.page = 1
  fetchOperationLogs()
}

// 处理搜索
const handleSearch = () => {
  queryParams.page = 1
  fetchOperationLogs()
}

// 重置搜索条件
const resetSearch = () => {
  queryParams.operation_type = undefined
  queryParams.operation_model = undefined
  queryParams.user = undefined
  queryParams.search = undefined
  queryParams.page = 1
  fetchOperationLogs()
}

// 格式化日期时间
const formatDateTime = (row: OperationLog, column: TableColumnCtx<OperationLog>) => {
  const date = new Date(row.operation_time)
  return date.toLocaleString()
}

// 格式化浏览器信息，显示前30个字符
const formatUserAgent = (row: OperationLog) => {
  if (!row.user_agent) return ''
  return row.user_agent.length > 30 
    ? `${row.user_agent.substring(0, 30)}...` 
    : row.user_agent
}

onMounted(() => {
  fetchOperationLogs()
})
</script>

<template>
  <div class="operation-log-container">
    <h2>操作日志管理</h2>
    
    <!-- 搜索表单 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="queryParams" class="search-form">
        <el-form-item label="操作类型">
          <el-select v-model="queryParams.operation_type" placeholder="请选择操作类型" clearable>
            <el-option 
              v-for="item in operationTypeOptions" 
              :key="item.value" 
              :label="item.label" 
              :value="item.value" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="操作模块">
          <el-input v-model="queryParams.operation_model" placeholder="请输入操作模块" clearable />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="queryParams.search" placeholder="请输入关键词" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table 
        :data="tableData" 
        style="width: 100%" 
        border 
        v-loading="loading"
        stripe
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="操作用户" width="120">
          <template #default="{row}">
            {{ row.user ? row.user.username : '未知用户' }}
          </template>
        </el-table-column>
        <el-table-column prop="operation_type_display" label="操作类型" width="100" />
        <el-table-column prop="operation_model" label="操作模块" width="120" />
        <el-table-column prop="request_path" label="请求地址" width="180" />
        <el-table-column prop="request_method" label="请求方法" width="100" />
        <el-table-column label="操作浏览器" width="180">
          <template #default="{row}">
            <el-tooltip 
              :content="row.user_agent" 
              placement="top" 
              :hide-after="0"
              v-if="row.user_agent && row.user_agent.length > 30"
            >
              <span>{{ formatUserAgent(row) }}</span>
            </el-tooltip>
            <span v-else>{{ row.user_agent }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="response_code" label="响应码" width="100" />
        <el-table-column prop="ip_address" label="IP地址" width="130" />
        <el-table-column prop="operation_time" label="操作时间" width="180" :formatter="formatDateTime" />
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.page"
          v-model:page-size="queryParams.page_size"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.operation-log-container {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>