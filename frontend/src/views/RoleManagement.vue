<template>
  <div class="role-management">
    <div class="header">
      <h2>角色管理</h2>
      <el-button type="primary" @click="showRoleDialog('create')">新增角色</el-button>
    </div>

    <el-table :data="roles" style="width: 100%">
      <el-table-column prop="name" label="角色名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column label="创建时间">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="showRoleDialog('edit', row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          <el-button type="info" size="small" @click="showAssignUserDialog(row)">分配用户</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 角色对话框 -->
    <el-dialog
      :title="dialogType === 'create' ? '新增角色' : '编辑角色'"
      v-model="roleDialogVisible"
      width="500px"
    >
      <el-form :model="roleForm" label-width="80px">
        <el-form-item label="角色名称" required>
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="roleForm.description"
            type="textarea"
            placeholder="请输入角色描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="roleDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveRole">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 分配用户对话框 -->
    <el-dialog title="分配用户" v-model="assignUserDialogVisible" width="600px">
      <el-transfer
        v-model="selectedUsers"
        :data="allUsers"
        :titles="['未分配用户', '已分配用户']"
        :props="{
          key: 'id',
          label: 'username'
        }"
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="assignUserDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAssignUsers">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getRoles, createRole, updateRole, deleteRole, assignUsers } from '@/api/role'
import { getUsers } from '@/api/user'

const roles = ref([])
const roleDialogVisible = ref(false)
const assignUserDialogVisible = ref(false)
const dialogType = ref('create')
const currentRole = ref<any>(null)
const allUsers = ref<any>([])
const selectedUsers = ref([])

const roleForm = ref({
  name: '',
  description: ''
})

// 获取角色列表
const fetchRoles = async () => {
  try {
    const response = await getRoles()
    roles.value = response.data.results
  } catch (error) {
    ElMessage.error('获取角色列表失败')
  }
}

// 获取用户列表
const fetchUsers = async () => {
  try {
    const response = await getUsers()
    allUsers.value = response.results.map((user: any) => ({
      id: user.id,
      username: user.username
    }))
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  }
}

// 显示角色对话框
const showRoleDialog = (type: 'create' | 'edit', role: any = null) => {
  dialogType.value = type
  if (type === 'edit' && role) {
    roleForm.value = { ...role }
    currentRole.value = role
  } else {
    roleForm.value = { name: '', description: '' }
    currentRole.value = null
  }
  roleDialogVisible.value = true
}

// 保存角色
const handleSaveRole = async () => {
  try {
    if (dialogType.value === 'create') {
      await createRole(roleForm.value)
      ElMessage.success('创建角色成功')
    } else {
      await updateRole(currentRole.value?.id, roleForm.value)
      ElMessage.success('更新角色成功')
    }
    roleDialogVisible.value = false
    fetchRoles()
  } catch (error) {
    ElMessage.error(dialogType.value === 'create' ? '创建角色失败' : '更新角色失败')
  }
}

// 删除角色
const handleDelete = (role: any) => {
  ElMessageBox.confirm('确认删除该角色？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteRole(role.id)
      ElMessage.success('删除角色成功')
      fetchRoles()
    } catch (error) {
      ElMessage.error('删除角色失败')
    }
  })
}

// 显示分配用户对话框
const showAssignUserDialog = async (role: any) => {
  currentRole.value = role
  selectedUsers.value = role.users.map((id: any) => id)
  await fetchUsers()
  assignUserDialogVisible.value = true
}

// 分配用户
const handleAssignUsers = async () => {
  try {
    await assignUsers(currentRole.value.id, selectedUsers.value)
    ElMessage.success('分配用户成功')
    assignUserDialogVisible.value = false
    fetchRoles()
  } catch (error) {
    ElMessage.error('分配用户失败')
  }
}

// 格式化日期
const formatDate = (date: string) => {
  return new Date(date).toLocaleString()
}

onMounted(() => {
  fetchRoles()
})
</script>

<style scoped>
.role-management {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>