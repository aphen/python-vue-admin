<template>
  <div class="blog-detail">
    <el-card v-if="blogPost">
      <div class="blog-header">
        <el-button @click="router.back()" type="primary" size="small" class="back-button">
          <el-icon><ArrowLeft /></el-icon> 返回列表
        </el-button>
        <h1 class="blog-title">{{ blogPost.title }}</h1>
        <div class="blog-meta">
          <span>作者：{{ blogPost.author?.username }}</span>
          <span>发布时间：{{ formatDate(blogPost.created_at) }}</span>
          <span v-if="blogPost.updated_at !== blogPost.created_at">
            更新时间：{{ formatDate(blogPost.updated_at) }}
          </span>
        </div>
        <div class="blog-actions" v-if="blogPost.author && isAuthorOrAdmin(blogPost.author.id)">
          <el-button 
            type="primary" 
            size="small" 
            @click="handleEdit(blogPost.id)"
          >
            <el-icon><Edit /></el-icon> 编辑
          </el-button>
          <el-button 
            type="danger" 
            size="small" 
            @click="handleDelete(blogPost.id, blogPost.title)"
          >
            <el-icon><Delete /></el-icon> 删除
          </el-button>
        </div>
      </div>
      <div class="blog-content" v-html="blogPost.content"></div>
        <div class="blog-comments">
          <h3>评论区</h3>
          <div v-if="userStore.isAuthenticated" class="comment-form">
            <el-input
              v-model="newComment"
              type="textarea"
              :rows="3"
              placeholder="写下你的评论..."
            />
            <el-button type="primary" @click="submitComment" :loading="submitting">
              发表评论
            </el-button>
          </div>
          <div v-else class="login-prompt">
            <el-alert
              title="请登录后发表评论"
              type="info"
              :closable="false"
              show-icon
            />
          </div>
          <div class="comments-list">
            <div v-if="comments.length === 0" class="no-comments">
              暂无评论
            </div>
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <div class="comment-header">
                <span class="comment-author">{{ comment.author.username }}</span>
                <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                <el-button
                  v-if="isAuthorOrAdmin(comment.author.id)"
                  type="danger"
                  size="small"
                  @click="deleteComment(comment.id)"
                >
                  删除
                </el-button>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
        </div>
    </el-card>
    <div v-else class="loading-container">
      <el-empty description="加载中..." />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Edit, Delete } from '@element-plus/icons-vue'
import { getBlogPost, deleteBlogPost, getBlogComments, createBlogComment, deleteBlogComment } from '@/api/blog'
import { useUserStore } from '@/store/user'
import type{ BlogComment } from '@/api/blog'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const blogPost = ref<any>({})
const comments = ref<BlogComment[]>([])
const newComment = ref('')
const submitting = ref(false)

// 创建一个简单的日期格式化函数
const formatDate = (date: string) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// 判断当前用户是否是文章作者或管理员
const isAuthorOrAdmin = (authorId: number) => {
  // 判断用户是否是管理员或文章作者
  // 管理员判断逻辑：检查用户是否有is_staff或is_superuser属性为true
  const isAdmin = userStore.is_staff || userStore.is_superuser
  const isAuthor = userStore.id === authorId
  return isAdmin || isAuthor
}

// 跳转到编辑文章页面
const handleEdit = (id: number) => {
  router.push(`/blog/create?id=${id}`)
}

// 删除文章
const handleDelete = (id: number, title: string) => {
  ElMessageBox.confirm(
    `确定要删除文章 "${title}" 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      try {
        await deleteBlogPost(id)
        ElMessage.success('删除成功')
        router.push('/blog/list')
      } catch (error) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}

const fetchBlogPost = async () => {
  try {
    const response = await getBlogPost(route.params.id as string)
    blogPost.value = response.data
  } catch (error) {
    ElMessage.error('获取博客详情失败')
  }
}

// 获取评论列表
const fetchComments = async () => {
  try {
    const response = await getBlogComments(route.params.id as string)
    comments.value = response.data.results
  } catch (error) {
    ElMessage.error('获取评论失败')
  }
}

// 提交评论
const submitComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  submitting.value = true
  try {
    await createBlogComment({
      post: Number(route.params.id),
      content: newComment.value,
      author_id: userStore.id!
    })
    ElMessage.success('评论发表成功')
    newComment.value = ''
    await fetchComments()
  } catch (error) {
    ElMessage.error('评论发表失败')
  } finally {
    submitting.value = false
  }
}

// 删除评论
const deleteComment = async (commentId: number) => {
  try {
    await deleteBlogComment(commentId)
    ElMessage.success('评论删除成功')
    await fetchComments()
  } catch (error) {
    ElMessage.error('评论删除失败')
  }
}

onMounted(() => {
  fetchBlogPost()
  fetchComments()
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
  position: relative;
}

.back-button {
  position: absolute;
  top: 0;
  right: 0;
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
  max-height: 700px;
  overflow-y: auto;
  padding-right: 10px;
}

.blog-comments {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--el-border-color-light);
}

.comment-form {
  margin-bottom: 20px;
}

.comment-form .el-button {
  margin-top: 10px;
}

.login-prompt {
  margin-bottom: 20px;
}

.comments-list {
  margin-top: 20px;
}

.comment-item {
  margin-bottom: 20px;
  padding: 15px;
  background-color: var(--el-bg-color-page);
  border-radius: 4px;
}

.comment-header {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.comment-author {
  font-weight: bold;
  margin-right: 10px;
}

.comment-time {
  color: var(--el-text-color-secondary);
  font-size: 14px;
  flex-grow: 1;
}

.comment-content {
  line-height: 1.6;
}

.no-comments {
  text-align: center;
  color: var(--el-text-color-secondary);
  padding: 20px 0;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}
</style>