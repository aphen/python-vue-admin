<template>
  <div class="blog-create">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>发布文章</span>
        </div>
      </template>
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入文章标题" />
        </el-form-item>
        <el-form-item label="摘要" prop="summary">
          <el-input
            v-model="formData.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要"
          />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <div class="editor-container">
            <editor-content :editor="editor" />
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">发布文章</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { EditorContent, Editor } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { createBlogPost } from '@/api/blog'

const editor = new Editor({
    extensions: [StarterKit],
    content: '<p>Hello World!</p>',
})
const router = useRouter()
const formRef = ref()

const formData = reactive({
  title: '',
  summary: '',
  content: ''
})

const rules = {
  title: [{ required: true, message: '请输入文章标题', trigger: 'blur' }],
  summary: [{ required: true, message: '请输入文章摘要', trigger: 'blur' }],
  content: [{ required: true, message: '请输入文章内容', trigger: 'blur' }]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        await createBlogPost(formData)
        ElMessage.success('文章发布成功')
        router.push('/blog/list')
      } catch (error) {
        ElMessage.error('文章发布失败')
      }
    }
  })
}

const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}
</script>

<style scoped>
.blog-create {
  padding: 20px;
}

.editor-container {
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
}

.editor-container :deep(.el-tiptap) {
  min-height: 400px;
}
</style>