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
      <el-row>
        <el-col v-for="post in blogPosts" :key="post.id" :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb-4">
          <div class="blog-card">
            <div class="blog-card-header">
              <router-link :to="`/blog/detail/${post.id}`" class="blog-title-link">
                <h3 class="blog-title">{{ post.title }}</h3>
              </router-link>
            </div>
            <div class="blog-card-content">
              <p class="blog-summary">{{ post.summary }}</p>
              <div class="blog-meta">
                <div class="blog-info">
                  <span class="author">{{ post.author.username }}</span>
                  <span class="date">{{ formatDate(post.created_at) }}</span>
                </div>
                <div class="blog-tags">
                  <el-tag
                    v-for="tag in post.tags"
                    :key="tag.id"
                    size="small"
                    class="mx-1"
                  >
                    {{ tag.name }}
                  </el-tag>
                </div>
              </div>
            </div>
            <div class="blog-card-actions" v-if="isAuthorOrAdmin(post.author.id)">
              <el-button type="primary" size="small" @click="handleEdit(post.id)">
                <el-icon><Edit /></el-icon> 编辑
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(post.id, post.title!)">
                <el-icon><Delete /></el-icon> 删除
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>
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
  margin-bottom: 24px;
}

.mb-4 {
  margin-bottom: 0;
  padding: 24px 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.mb-4:last-child {
  border-bottom: none;
}

.blog-card {
  height: 100%;
}

.blog-card-header {
  margin-bottom: 16px;
}

.blog-title {
  margin: 0;
  font-size: 20px;
  line-height: 1.4;
  font-weight: 600;
}

.blog-card-content {
  margin-bottom: 16px;
}

.blog-summary {
  margin: 12px 0;
  color: var(--el-text-color-regular);
  font-size: 14px;
  line-height: 1.6;
}

.blog-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.blog-info {
  display: flex;
  justify-content: space-between;
}

.blog-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  margin-bottom: 12px;
}

.blog-card-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.blog-title-link {
  color: var(--el-text-color-primary);
  text-decoration: none;
}

.blog-title-link:hover {
  color: var(--el-color-primary);
  text-decoration: none;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>