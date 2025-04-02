import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';

interface UserState {
  username: string;
  email: string;
  date_joined: string;
  isAuthenticated: boolean;
}

export const useUserStore = defineStore('user', () => {
  const username = ref('');
  const email = ref('');
  const date_joined = ref('');
  const isAuthenticated = ref(false);

  function setUserInfo(userInfo: Partial<UserState>) {
    if (userInfo.username !== undefined) username.value = userInfo.username;
    if (userInfo.email !== undefined) email.value = userInfo.email;
    if (userInfo.date_joined !== undefined) date_joined.value = userInfo.date_joined;
    if (userInfo.isAuthenticated !== undefined) isAuthenticated.value = userInfo.isAuthenticated;

    // 保存用户信息到localStorage
    localStorage.setItem(
      'userInfo',
      JSON.stringify({
        username: username.value,
        email: email.value,
        date_joined: date_joined.value,
        isAuthenticated: isAuthenticated.value,
      })
    );
  }

  function clearUserInfo() {
    username.value = '';
    email.value = '';
    date_joined.value = '';
    isAuthenticated.value = false;
    localStorage.removeItem('userInfo');
  }

  async function initUserInfo() {
    // 从localStorage恢复用户信息
    const storedInfo = localStorage.getItem('userInfo');
    if (storedInfo) {
      const userInfo = JSON.parse(storedInfo);
      setUserInfo(userInfo);

      // 如果有token，重新获取用户信息以确保最新
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const response = await api.get('/polls/api/users/me/');
          setUserInfo({
            ...response.data,
            isAuthenticated: true,
          });
        } catch (error) {
          console.error('获取用户信息失败:', error);
          clearUserInfo();
        }
      }
    }
  }

  return {
    username,
    email,
    date_joined,
    isAuthenticated,
    setUserInfo,
    clearUserInfo,
    initUserInfo,
  };
});
