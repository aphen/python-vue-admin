declare module '@wangeditor/editor-for-vue' {
  import { Component } from 'vue'
  
  export const Editor: Component
  export const Toolbar: Component
}

declare module '@wangeditor/editor' {
  export interface IEditorConfig {
    placeholder?: string
    [key: string]: any
  }
  
  export interface IToolbarConfig {
    [key: string]: any
  }
}