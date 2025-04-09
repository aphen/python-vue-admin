<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { Plus, Edit, Delete } from '@element-plus/icons-vue'
import type { Department } from '../api/department'
import { getDepartmentList, createDepartment, updateDepartment, deleteDepartment } from '../api/department'

// interface Department {
//   id: number
//   name: string
//   parent: number | null
//   parent_name: string | null
//   order: number
//   children?: Department[]
// }

const departments = ref<Department[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加部门')
const formRef = ref<FormInstance>()
const form = ref({
  id: undefined as number | undefined,
  name: '',
  parent: null as number | null,
  order: 0
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入部门名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ]
}

const fetchDepartments = async () => {
  try {
    const response = await getDepartmentList()
    departments.value = response.data.results
  } catch (error) {
    ElMessage.error('获取部门列表失败')
  }
}

const handleAdd = (row?: Department) => {
  dialogTitle.value = '添加部门'
  form.value = {
    id: undefined,
    name: '',
    parent: row?.id || null,
    order: 0
  }
  dialogVisible.value = true
}

const handleEdit = (row: Department) => {
  dialogTitle.value = '编辑部门'
  form.value = {
    id: row.id,
    name: row.name,
    parent: row.parent,
    order: row.order
  }
  dialogVisible.value = true
}

const handleDelete = (row: Department) => {
  ElMessageBox.confirm('确认删除该部门吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteDepartment(row.id)
        ElMessage.success('删除成功')
        fetchDepartments()
      } catch (error) {
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {})
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (form.value.id) {
          await updateDepartment(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await createDepartment(form.value)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        fetchDepartments()
      } catch (error: any) {
        console.log(error)
        ElMessage.error(form.value.id ? '更新失败' : error.response.data.msg)
      }
    }
  })
}

onMounted(() => {
  fetchDepartments()
})
</script>

<template>
  <div class="department-container">
    <div class="header">
      <h2>部门管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleAdd()">添加部门</el-button>
    </div>

    <el-table :data="departments" row-key="id" border default-expand-all>
      <el-table-column prop="name" label="部门名称" min-width="180" />
      <el-table-column prop="parent_name" label="上级部门" min-width="180" />
      <el-table-column prop="order" label="排序" width="100" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="text" :icon="Plus" @click="handleAdd(row)">添加</el-button>
          <el-button type="text" :icon="Edit" @click="handleEdit(row)">编辑</el-button>
          <el-button type="text" :icon="Delete" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="上级部门">
          <el-tree-select
            v-model="form.parent"
            :data="departments"
            :props="{
              value: 'id',
              label: 'name',
              children: 'children'
            }"
            placeholder="请选择上级部门"
            clearable
            check-strictly
          />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.order" :min="0" :max="999" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.department-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
}
</style>