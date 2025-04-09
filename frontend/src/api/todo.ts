import request from './index'
export interface Todo {
  content: string
  completed: boolean
}

export const addTodo = (data: Todo) => {
  return request.post<Todo>('/polls/api/todos/', data) 
}

export const getUncompletedTodos = () => {
  return request.get<{results: Todo[]}>('/polls/api/todos/uncompleted_todos/')
}
export const getCompletedTodos = () => {
  return request.get<{results: Todo[]}>('/polls/api/todos/completed_todos/') 
}
export const delTodo = (id: number) => {
  return request.delete<Todo>(`/polls/api/todos/${id}/`)
}
// mark as completed
export const markTodo = (id: number, data: Todo) => {
  return request.put<Todo>(`/polls/api/todos/${id}/`, data)
}
// clear completed
export const clearCompleted = () => {
  return request.delete('/polls/api/todos/clear_completed/')
}