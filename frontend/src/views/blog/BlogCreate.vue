<template>
  <div class="blog-create">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑文章' : '发布文章' }}</span>
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
          <div style="border: 1px solid #ccc">
            <Toolbar
              style="border-bottom: 1px solid #ccc"
              :editor="editorRef"
              :defaultConfig="toolbarConfig"
              :mode="mode"
            />
            <Editor
              style="height: 500px; overflow-y: hidden;"
              v-model="formData.content"
              :defaultConfig="editorConfig"
              :mode="mode"
              @onCreated="handleCreated"
            />
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">{{ isEdit ? '保存修改' : '发布文章' }}</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button v-if="isEdit" @click="router.push('/blog/list')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, shallowRef, onBeforeUnmount, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createBlogPost, getBlogPost, updateBlogPost } from '@/api/blog'
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import type { IEditorConfig, IToolbarConfig } from '@wangeditor/editor'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const editorRef = shallowRef()

// 判断是否为编辑模式
const blogId = computed(() => route.query.id ? Number(route.query.id) : undefined)
const isEdit = computed(() => !!blogId.value)

// 编辑器配置
const mode = 'default'
const editorConfig: Partial<IEditorConfig> = {
  placeholder: '请输入内容...'
}
const toolbarConfig: Partial<IToolbarConfig> = {}

const formData = reactive({
  title: '',
  summary: '',
  content: ''
})

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})

const handleCreated = (editor: any) => {
  editorRef.value = editor
}

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
        if (isEdit.value && blogId.value) {
          await updateBlogPost(blogId.value, formData)
          ElMessage.success('文章更新成功')
        } else {
          await createBlogPost(formData)
          ElMessage.success('文章发布成功')
        }
        router.push('/blog/list')
      } catch (error) {
        ElMessage.error(isEdit.value ? '文章更新失败' : '文章发布失败')
      }
    }
  })
}

const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 获取博客文章详情
const fetchBlogPost = async () => {
  if (!blogId.value) return
  
  try {
    const response = await getBlogPost(blogId.value)
    const blogData = response.data
    
    // 填充表单数据
    formData.title = blogData.title || ''
    formData.summary = blogData.summary || ''
    formData.content = blogData.content || ''
  } catch (error) {
    ElMessage.error('获取文章详情失败')
    router.push('/blog/list')
  }
}

onMounted(() => {
  if (isEdit.value) {
    fetchBlogPost()
  }
})
</script>

<style scoped>
.blog-create {
  padding: 20px;
}


</style>