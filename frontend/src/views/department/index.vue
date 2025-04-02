<template>
  <div class="department-container">
    <div class="department-header">
      <el-button type="primary" @click="handleAdd">新增部门</el-button>
    </div>

    <el-table
      :data="departmentList"
      row-key="id"
      border
      :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
    >
      <el-table-column prop="name" label="部门名称" width="220" />
      <el-table-column prop="parent_name" label="上级部门" width="220" />
      <el-table-column prop="order" label="排序" width="100" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column prop="updated_at" label="更新时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增部门' : '编辑部门'"
      width="500px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="上级部门" prop="parent">
          <el-tree-select
            v-model="form.parent"
            :data="departmentOptions"
            :props="{ label: 'name', value: 'id' }"
            placeholder="请选择上级部门"
            clearable
            check-strictly
          />
        </el-form-item>
        <el-form-item label="排序" prop="order">
          <el-input-number v-model="form.order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import type { Department, DepartmentForm } from '@/api/department'
import { getDepartmentList, createDepartment, updateDepartment, deleteDepartment } from '@/api/department'

const departmentList = ref<Department[]>([])
const departmentOptions = ref<Department[]>([])
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()

const form = ref<DepartmentForm>({
  name: '',
  parent: null,
  order: 0
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入部门名称', trigger: 'blur' }]
}

const fetchDepartmentList = async () => {
  try {
    const response = await getDepartmentList()
    departmentList.value = response.data
    departmentOptions.value = response.data
  } catch (error) {
    console.error('获取部门列表失败:', error)
    ElMessage.error('获取部门列表失败')
  }
}

const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    name: '',
    parent: null,
    order: 0
  }
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  form.value = {
    id: row.id,
    name: row.name,
    parent: row.parent,
    order: row.order
  }
  dialogVisible.value = true
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm('确认删除该部门吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      try {
        await deleteDepartment(row.id)
        ElMessage.success('删除成功')
        fetchDepartmentList()
      } catch (error) {
        console.error('删除部门失败:', error)
        ElMessage.error('删除部门失败')
      }
    })
    .catch(() => {
      // 取消删除操作
    })
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          await createDepartment(form.value)
          ElMessage.success('新增成功')
        } else {
          await updateDepartment(form.value.id!, form.value)
          ElMessage.success('编辑成功')
        }
        dialogVisible.value = false
        fetchDepartmentList()
      } catch (error) {
        console.error('保存部门失败:', error)
        ElMessage.error('保存部门失败')
      }
    }
  })
}

onMounted(() => {
  fetchDepartmentList()
})
</script>

<style scoped>
.department-container {
  padding: 20px;
}

.department-header {
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>