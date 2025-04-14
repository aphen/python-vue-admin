<template>
  <div class="blog-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>博客文章列表</span>
          <el-button 
            v-if="userStore.isAuthenticated" 
            type="primary" 
            @click="goToCreate"
          >
            <el-icon><Plus /></el-icon> 发布文章
          </el-button>
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
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button 
                v-if="isAuthorOrAdmin(row.author.id)" 
                type="primary" 
                size="small" 
                @click="handleEdit(row.id)"
              >
                <el-icon><Edit /></el-icon> 编辑
              </el-button>
              <el-button 
                v-if="isAuthorOrAdmin(row.author.id)" 
                type="danger" 
                size="small" 
                @click="handleDelete(row.id, row.title)"
              >
                <el-icon><Delete /></el-icon> 删除
              </el-button>
            </div>
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import { getBlogPosts, deleteBlogPost } from '@/api/blog'
import type { BlogPost } from '@/api/blog'
// 使用dayjs库格式化日期
import dayjs from 'dayjs'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const blogPosts = ref<BlogPost[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchBlogPosts = async () => {
  try {
    const response = await getBlogPosts({
      page: currentPage.value,
      page_size: pageSize.value
    })
    blogPosts.value = response.data.results
    total.value = response.data.count
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

// 判断当前用户是否是文章作者或管理员
const isAuthorOrAdmin = (authorId: number) => {
  // 判断用户是否是管理员或文章作者
  // 管理员判断逻辑：检查用户是否有is_staff或is_superuser属性为true
  const isAdmin = userStore.is_staff || userStore.is_superuser
  const isAuthor = userStore.id === authorId
  return isAdmin || isAuthor
}

// 跳转到创建文章页面
const goToCreate = () => {
  router.push('/blog/create')
}

// 跳转到编辑文章页面
const handleEdit = (id: number) => {
  router.push(`/blog/create?id=${id}`)
}

// 删除文章
const handleDelete = (id: number, title: string) => {
  ElMessageBox.confirm(
    `确定要删除文章 "${title}" 吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await deleteBlogPost(id)
      ElMessage.success('删除成功')
      fetchBlogPosts()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    ElMessage.info('已取消删除')
  })
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

.action-buttons {
  display: flex;
  gap: 8px;
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