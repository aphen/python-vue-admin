<template>
  <div class="blog-detail">
    <el-card v-if="blogPost">
      <div class="blog-header">
        <h1 class="blog-title">{{ blogPost.title }}</h1>
        <div class="blog-meta">
          <span>作者：{{ blogPost.author?.username }}</span>
          <span>发布时间：{{ formatDate(blogPost.created_at) }}</span>
          <span v-if="blogPost.updated_at !== blogPost.created_at">
            更新时间：{{ formatDate(blogPost.updated_at) }}
          </span>
        </div>
      </div>
      <div class="blog-content" v-html="blogPost.content"></div>
    </el-card>
    <div v-else class="loading-container">
      <el-empty description="加载中..." />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getBlogPost } from '@/api/blog'
import { formatDate } from '@/utils/date'

const route = useRoute()
const blogPost = ref(null)

const fetchBlogPost = async () => {
  try {
    const response = await getBlogPost(route.params.id)
    blogPost.value = response
  } catch (error) {
    ElMessage.error('获取博客详情失败')
  }
}

onMounted(() => {
  fetchBlogPost()
})
</script>

<style scoped>
.blog-detail {
  padding: 20px;
}

.blog-header {
  margin-bottom: 30px;
  border-bottom: 1px solid var(--el-border-color-light);
  padding-bottom: 20px;
}

.blog-title {
  margin: 0 0 15px;
  font-size: 28px;
  color: var(--el-text-color-primary);
}

.blog-meta {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.blog-meta span {
  margin-right: 20px;
}

.blog-content {
  line-height: 1.8;
  font-size: 16px;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}
</style>