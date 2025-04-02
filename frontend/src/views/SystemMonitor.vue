<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import api from '@/api'

// 定义系统资源数据类型
interface DiskInfo {
  total: number
  used: number
  percent: number
  mountpoint: string
  fstype: string
}

interface SystemResource {
  cpu: {
    percent: number
  }
  memory: {
    total: number
    used: number
    percent: number
  }
  disks: Record<string, DiskInfo>
}

// 初始化数据
const systemData = ref<SystemResource | null>(null)
const loading = ref(true)
const cpuChart = ref<HTMLElement | null>(null)
const memoryChart = ref<HTMLElement | null>(null)
const diskCharts = ref<Record<string, HTMLElement | null>>({}) // 存储多个磁盘图表的引用
let cpuChartInstance: echarts.ECharts | null = null
let memoryChartInstance: echarts.ECharts | null = null
let diskChartInstances: Record<string, echarts.ECharts | null> = {} // 存储多个磁盘图表实例
let timer: number | null = null

// 格式化字节大小
const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 创建图表选项的通用函数
const createGaugeOption = (name: string) => {
  return {
    series: [{
      type: 'gauge',
      startAngle: 90,
      endAngle: -270,
      pointer: {
        show: false
      },
      progress: {
        show: true,
        overlap: false,
        roundCap: true,
        clip: false,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0,
              color: '#67C23A'
            }, {
              offset: 0.7,
              color: '#E6A23C'
            }, {
              offset: 1,
              color: '#F56C6C'
            }]
          }
        }
      },
      axisLine: {
        lineStyle: {
          width: 20
        }
      },
      splitLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        show: false
      },
      title: {
        fontSize: 14
      },
      detail: {
        width: 50,
        height: 14,
        fontSize: 20,
        color: '#303133',
        formatter: '{value}%'
      },
      data: [{
        value: 0,
        name: name
      }]
    }]
  }
}

// 初始化图表
const initCharts = () => {
  if (cpuChart.value && memoryChart.value) {
    // 初始化CPU图表
    cpuChartInstance = echarts.init(cpuChart.value)
    cpuChartInstance.setOption(createGaugeOption('CPU'))

    // 初始化内存图表
    memoryChartInstance = echarts.init(memoryChart.value)
    memoryChartInstance.setOption(createGaugeOption('内存'))
  }
}

// 初始化磁盘图表
const initDiskCharts = () => {
  if (!systemData.value) return
  
  // 清除旧的图表实例
  Object.values(diskChartInstances).forEach(chart => chart?.dispose())
  diskChartInstances = {}
  
  // 为每个磁盘创建图表
  Object.keys(systemData.value.disks).forEach(diskKey => {
    const chartElement = diskCharts.value[diskKey]
    if (chartElement) {
      diskChartInstances[diskKey] = echarts.init(chartElement)
      diskChartInstances[diskKey]?.setOption(createGaugeOption(diskKey))
    }
  })
}

// 更新图表数据
const updateCharts = () => {
  if (!systemData.value) return

  if (cpuChartInstance) {
    cpuChartInstance.setOption({
      series: [{
        data: [{
          value: systemData.value.cpu.percent,
          name: 'CPU'
        }]
      }]
    })
  }

  if (memoryChartInstance) {
    memoryChartInstance.setOption({
      series: [{
        data: [{
          value: systemData.value.memory.percent,
          name: '内存'
        }]
      }]
    })
  }

  // 更新所有磁盘图表
  Object.entries(systemData.value.disks).forEach(([diskKey, diskInfo]) => {
    if (diskChartInstances[diskKey]) {
      diskChartInstances[diskKey]?.setOption({
        series: [{
          data: [{
            value: diskInfo.percent,
            name: diskKey
          }]
        }]
      })
    }
  })
}

// 获取系统资源数据
const fetchSystemData = async () => {
  try {
    const response = await api.get('/polls/api/system-monitor/')
    systemData.value = response.data
    loading.value = false
    
    // 如果是首次加载数据，初始化磁盘图表
    if (Object.keys(diskChartInstances).length === 0) {
      initDiskCharts()
    }
    
    updateCharts()
  } catch (error) {
    console.error('获取系统资源数据失败:', error)
    ElMessage.error('获取系统资源数据失败')
    loading.value = false
  }
}

// 处理窗口大小变化
const handleResize = () => {
  cpuChartInstance?.resize()
  memoryChartInstance?.resize()
  Object.values(diskChartInstances).forEach(chart => chart?.resize())
}

onMounted(() => {
  // 初始化图表
  initCharts()
  // 获取初始数据
  fetchSystemData()
  // 设置定时刷新
  timer = window.setInterval(fetchSystemData, 10000) // 每10秒刷新一次
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  // 清除定时器
  if (timer) {
    clearInterval(timer)
  }
  // 销毁图表实例
  cpuChartInstance?.dispose()
  memoryChartInstance?.dispose()
  Object.values(diskChartInstances).forEach(chart => chart?.dispose())
  // 移除事件监听
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div class="system-monitor">
    <h2>服务监控</h2>
    <el-card v-loading="loading">
      <div class="monitor-content">
        <div class="monitor-item">
          <div ref="cpuChart" class="chart"></div>
          <div class="info" v-if="systemData">
            <p>CPU使用率: {{ systemData.cpu.percent }}%</p>
          </div>
        </div>
        <div class="monitor-item">
          <div ref="memoryChart" class="chart"></div>
          <div class="info" v-if="systemData">
            <p>内存使用率: {{ systemData.memory.percent }}%</p>
            <p>总内存: {{ formatBytes(systemData.memory.total) }}</p>
            <p>已用内存: {{ formatBytes(systemData.memory.used) }}</p>
          </div>
        </div>
        <!-- 动态生成磁盘监控项 -->
        <div v-if="systemData" v-for="(diskInfo, diskKey) in systemData.disks" :key="diskKey" class="monitor-item">
          <div :ref="el => { if (el) diskCharts[diskKey] = el as HTMLElement }" class="chart"></div>
          <div class="info">
            <p><strong>{{ diskKey }}</strong> 使用率: {{ diskInfo.percent }}%</p>
            <p>总容量: {{ formatBytes(diskInfo.total) }}</p>
            <p>已用容量: {{ formatBytes(diskInfo.used) }}</p>
            <p>挂载点: {{ diskInfo.mountpoint }}</p>
            <p>文件系统: {{ diskInfo.fstype }}</p>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.system-monitor {
  padding: 20px;
}

.monitor-content {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-between;
}

.monitor-item {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart {
  width: 300px;
  height: 300px;
}

.info {
  margin-top: 20px;
  text-align: center;
}

@media (max-width: 768px) {
  .monitor-content {
    flex-direction: column;
  }
}
</style>