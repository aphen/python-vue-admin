<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Check, Delete, RefreshRight } from '@element-plus/icons-vue'
import { addTodo as addTodos, getUncompletedTodos, getCompletedTodos, delTodo, markTodo, clearCompleted } from '@/api/todo'

interface TodoItem {
  id?: number | null
  createdAt?: string
  content: string
  completed: boolean
}

// 待办事项列表
const todoList = ref<TodoItem[]>([])
// 已完成事项列表
const completedList = ref<TodoItem[]>([])
// 新待办事项内容
const newTodo = ref('')

// 生成唯一ID
const generateId = () => {
  return Date.now()
}

// 格式化日期
const formatDate = () => {
  const date = new Date()
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 从本地存储加载数据
const loadTodos = () => {
    getUncompletedTodos().then((res) => {
        todoList.value = res.data.results
    })
    getCompletedTodos().then((res) => {
        completedList.value = res.data.results 
    })
//   const savedTodos = localStorage.getItem('todos')
//   const savedCompleted = localStorage.getItem('completedTodos')
  
//   if (savedTodos) {
//     todoList.value = JSON.parse(savedTodos)
//   }
  
//   if (savedCompleted) {
//     completedList.value = JSON.parse(savedCompleted)
//   }
}

// 保存数据到本地存储
const saveTodos = () => {
  localStorage.setItem('todos', JSON.stringify(todoList.value))
  localStorage.setItem('completedTodos', JSON.stringify(completedList.value))
}

// 添加新待办事项
const addTodo = () => {
  if (!newTodo.value.trim()) {
    ElMessage.warning('待办事项内容不能为空')
    return
  }
  
  const todo: TodoItem = {
    // id: generateId(),
    content: newTodo.value.trim(),
    completed: false,
    // createdAt: formatDate()
  }
  

  addTodos(todo).then(() => {
    todoList.value.unshift(todo)
    newTodo.value = ''
    ElMessage.success('添加成功') 
  })
  //   todoList.value.unshift(todo)
  // newTodo.value = ''
//   saveTodos()
 // ElMessage.success('添加成功')
}

// 完成待办事项
const completeTodo = (todo: TodoItem) => {
    todo.completed = true;
    markTodo(todo.id!, todo).then(() => {
        todoList.value = todoList.value.filter(item => item.id!== todo.id)
        completedList.value.unshift(todo) 
        ElMessage.success('已完成')
    })
//   // 从待办列表中移除
//   todoList.value = todoList.value.filter(item => item.id !== todo.id)
  
//   // 添加到已完成列表
//   todo.completed = true
//   completedList.value.unshift(todo)
  
//   saveTodos()
 // ElMessage.success('已完成')
}

// 删除待办事项
const deleteTodo = (todo: TodoItem) => {
  ElMessageBox.confirm(
    '确定要删除该待办事项吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    delTodo(todo.id!).then(() => {
        todoList.value = todoList.value.filter(item => item.id!== todo.id)
        ElMessage.success('删除成功') 
    })
    // todoList.value = todoList.value.filter(item => item.id !== todo.id)
    // saveTodos()
    //ElMessage.success('删除成功')
  }).catch(() => {
    // 用户取消，不做操作
  })
}

// 清除单个已完成事项
const clearCompletedTodo = (todo: TodoItem) => {
    delTodo(todo.id!).then(() => {
        completedList.value = completedList.value.filter(item => item.id!== todo.id)
        ElMessage.success('已清除') 
    })
//   completedList.value = completedList.value.filter(item => item.id !== todo.id)
//   saveTodos()
//   ElMessage.success('已清除')
}

// 清除所有已完成事项
const clearAllCompleted = () => {
  if (completedList.value.length === 0) {
    ElMessage.info('没有已完成的事项')
    return
  }
  
  ElMessageBox.confirm(
    '确定要清除所有已完成事项吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    clearCompleted().then(() => {
        completedList.value = []
        ElMessage.success('已清除所有完成事项') 
    })
    // completedList.value = []
    // saveTodos()
    // ElMessage.success('已清除所有完成事项')
  }).catch(() => {
    // 用户取消，不做操作
  })
}

// 组件挂载时加载数据
onMounted(() => {
  loadTodos()
})
</script>

<template>
  <div class="todo-container">
    <h1>待办事项管理</h1>
    
    <!-- 添加新待办 -->
    <div class="add-todo">
      <el-input 
        v-model="newTodo" 
        placeholder="请输入待办事项内容" 
        @keyup.enter="addTodo"
      >
        <template #append>
          <el-button @click="addTodo">添加</el-button>
        </template>
      </el-input>
    </div>
    
    <!-- 待办列表 -->
    <div class="todo-section">
      <h2>待办列表</h2>
      <el-empty v-if="todoList.length === 0" description="暂无待办事项"></el-empty>
      <el-card v-for="todo in todoList" :key="todo.id" class="todo-item">
        <div class="todo-content">
          <span>{{ todo.content }}</span>
          <span class="todo-time">{{ todo.createdAt }}</span>
        </div>
        <div class="todo-actions">
          <el-button 
            type="success" 
            size="small" 
            circle 
            @click="completeTodo(todo)"
            title="完成"
          >
            <el-icon><Check /></el-icon>
          </el-button>
          <el-button 
            type="danger" 
            size="small" 
            circle 
            @click="deleteTodo(todo)"
            title="删除"
          >
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </el-card>
    </div>
    
    <!-- 已完成列表 -->
    <div class="completed-section">
      <div class="completed-header">
        <h2>已完成列表</h2>
        <el-button 
          v-if="completedList.length > 0" 
          type="warning" 
          size="small" 
          @click="clearAllCompleted"
        >
          清除全部
        </el-button>
      </div>
      <el-empty v-if="completedList.length === 0" description="暂无已完成事项"></el-empty>
      <el-card v-for="todo in completedList" :key="todo.id" class="todo-item completed">
        <div class="todo-content">
          <span>{{ todo.content }}</span>
          <span class="todo-time">{{ todo.createdAt }}</span>
        </div>
        <div class="todo-actions">
          <el-button 
            type="danger" 
            size="small" 
            circle 
            @click="clearCompletedTodo(todo)"
            title="清除"
          >
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.todo-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #409EFF;
  margin-bottom: 30px;
}

h2 {
  color: #606266;
  margin-bottom: 15px;
}

.add-todo {
  margin-bottom: 30px;
}

.todo-section, .completed-section {
  margin-bottom: 40px;
}

.todo-item {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.todo-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.todo-time {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.todo-actions {
  display: flex;
  gap: 10px;
}

.completed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.completed .todo-content span:first-child {
  text-decoration: line-through;
  color: #909399;
}
</style>