<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, createUser, updateUser, deleteUser, type User } from '@/api/user'
import { getRoles } from '@/api/role'
import { getDepartmentList } from '@/api/department'

const getDepartmentPath = (department: any): string => {
  if (!department) return '-'
  return department.full_path
}

interface UserForm {
  username: string
  email: string
  password: string
  roles: { id: number; name: string }[]
  department: number | null
}

const dialogVisible = ref(false)
const isEdit = ref(false)
const currentRow = ref<any>();
const roles = ref<any[]>([])
const departments = ref<any[]>([])
const formData = ref<UserForm>({
  username: '',
  email: '',
  password: '',
  roles: [],
  department: null
})

const formRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  password: [{ required: !isEdit.value, message: '请输入密码', trigger: 'blur' }]
}

const users = ref<User[]>([])
const loading = ref(false)

const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await getUsers(currentPage.value, pageSize.value)
    users.value = res.results
    total.value = res.count || res.results.length
    console.log(users.value)
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchUsers()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchUsers()
}

const fetchRoles = async () => {
  try {
    const response = await getRoles()
    roles.value = response.data.results
  } catch (error) {
    ElMessage.error('获取角色列表失败')
  }
}

const handleEdit = async (row: User) => {
  isEdit.value = true
  dialogVisible.value = true
  currentRow.value = row;
  formData.value = {
    username: row.username,
    email: row.email,
    password: '',
    roles: row.roles.map((role: any) => role.id),
    department: (row as any).department?.id || null
  }
}

const resetForm = () => {
  formData.value = {
    username: '',
    email: '',
    password: '',
    roles: [],
    department: null
  }
  isEdit.value = false
  currentRow.value = null
}

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      const updateData = { ...formData.value }
      // if (updateData.department === null) {
      //   delete updateData.department
      // }
      await updateUser(currentRow.value.id, updateData)
      ElMessage.success('更新成功')
    } else {
      console.log(formData.value)
      await createUser(formData.value)
      // users.value.push(response)
      fetchUsers()
      ElMessage.success('新增用户成功')
    }
    fetchUsers()
    dialogVisible.value = false
    resetForm()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '新增用户失败')
  }
}

const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      type: 'warning'
     })
    await deleteUser(row.id)
    users.value = users.value.filter(user => user.id !== row.id)
    ElMessage.success('删除成功')
   } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
     }
   }
}

const fetchDepartments = async () => {
  try {
    const response = await getDepartmentList()
    departments.value = response.data.results
  } catch (error) {
    ElMessage.error('获取部门列表失败')
  }
}

onMounted(() => {
  fetchUsers()
  fetchRoles()
  fetchDepartments()
})

</script>

<template>
  <div class="user-list">
    <div class="header">
      <h2>用户列表</h2>
      <el-button type="primary" @click="dialogVisible = true">新增用户</el-button>
    </div>
    <el-table v-loading="loading" :data="users" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="roles" label="角色" width="180">
        <template #default="scope">
          <el-tag v-for="role in scope.row.roles" :key="role.id" style="margin-right: 5px">
            {{ role.name }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="department" label="部门" width="200">
        <template #default="scope">
          {{ getDepartmentPath(scope.row.department) }}
        </template>
      </el-table-column>
      <el-table-column prop="date_joined" label="注册时间" width="180" />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-container">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
      <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新增用户'" width="500px" @closed="resetForm">
      <el-form :model="formData" :rules="formRules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" autocomplete="off" />
        </el-form-item>
        <el-form-item v-if="!isEdit" label="密码" prop="password">
          <el-input v-model="formData.password" type="password" autocomplete="new-password" />
        </el-form-item>
        <el-form-item label="角色" prop="roles">
          <el-select v-model="formData.roles" multiple placeholder="请选择角色">
            <el-option
              v-for="role in roles"
              :key="role.id"
              :label="role.name"
              :value="role.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-tree-select
            v-model="formData.department"
            :data="departments"
            :props="{
              label: 'name',
              value: 'id',
              children: 'children'
            }"
            placeholder="请选择部门"
            check-strictly
          />
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

<style scoped>
.header {
  /* display: flex;
  justify-content: space-between;
  align-items: center; */
  margin-bottom: 20px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>