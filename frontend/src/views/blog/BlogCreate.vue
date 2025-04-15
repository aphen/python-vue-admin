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
        <el-form-item label="标签" prop="tags">
          <el-select
            v-model="formData.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请选择或创建标签"
            @visible-change="handleSelectVisibleChange"
          >
            <el-option
              v-for="tag in tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
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
import { getTags, createTag } from '@/api/tag'
import '@wangeditor/editor/dist/css/style.css'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import type { IEditorConfig, IToolbarConfig } from '@wangeditor/editor'
import type { Tag } from '@/api/tag'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const editorRef = shallowRef()

// 判断是否为编辑模式
const blogId = computed(() => route.query.id ? Number(route.query.id) : undefined)
const isEdit = computed(() => !!blogId.value)
const tags = ref<Tag[]>([])

// 编辑器配置
const mode = 'default'
const editorConfig: Partial<IEditorConfig> = {
  placeholder: '请输入内容...'
}
const toolbarConfig: Partial<IToolbarConfig> = {}

const formData = reactive<any>({
  title: '',
  summary: '',
  content: '',
  tags: []
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

// 处理标签选择框显示状态变化
const handleSelectVisibleChange = async (visible: boolean) => {
  if (!visible) {
    const newTags = formData.tags.filter((tag: string | number) => typeof tag === 'string')
    for (const newTagName of newTags) {
      try {
        const response = await createTag({ name: newTagName as string })
        const index = formData.tags.indexOf(newTagName)
        if (index !== -1) {
          formData.tags[index] = response.data.id
        }
        tags.value.push(response.data)
      } catch (error) {
        ElMessage.error(`创建标签 "${newTagName}" 失败`)
      }
    }
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
    formData.tags = blogData.tags?.map((tag: any) => tag.id) || []
  } catch (error) {
    ElMessage.error('获取文章详情失败')
    router.push('/blog/list')
  }
}

// 获取所有标签
const fetchTags = async () => {
  try {
    const response = await getTags()
    tags.value = response.data.results
  } catch (error) {
    ElMessage.error('获取标签列表失败')
  }
}

onMounted(() => {
  fetchTags()
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