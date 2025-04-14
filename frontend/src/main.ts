import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// 引入Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


// 引入Pinia
import { createPinia } from 'pinia'
const pinia = createPinia()

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.use(pinia)
app.mount('#app')
