<template>
  <div class="blog-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>博客文章列表</span>
        </div>
      </template>
      <el-table :data="blogPosts" style="width: 100%">
        <el-table-column prop="title" label="标题" min-width="200">
          <template #default="{ row }">
            <router-link :to="`/blog/detail/${row.id}`" class="blog-title-link">
              {{ row.title }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="summary" label="摘要" min-width="300" show-overflow-tooltip />
        <el-table-column prop="author.username" label="作者" width="120" />
        <el-table-column prop="created_at" label="发布时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getBlogPosts } from '@/api/blog'
// 使用dayjs库格式化日期
import dayjs from 'dayjs'

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const blogPosts = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchBlogPosts = async () => {
  try {
    const response = await getBlogPosts({
      page: currentPage.value,
      page_size: pageSize.value
    })
    blogPosts.value = response.results
    total.value = response.count
  } catch (error) {
    ElMessage.error('获取博客列表失败')
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchBlogPosts()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchBlogPosts()
}

onMounted(() => {
  fetchBlogPosts()
})
</script>

<style scoped>
.blog-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.blog-title-link {
  color: var(--el-color-primary);
  text-decoration: none;
}

.blog-title-link:hover {
  text-decoration: underline;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>