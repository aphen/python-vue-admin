import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';

interface UserState {
  id?: number;
  username: string;
  email: string;
  date_joined: string;
  isAuthenticated: boolean;
  is_staff?: boolean;
  is_superuser?: boolean;
  permissions?: string[];
  roles?: any[];
}

export const useUserStore = defineStore('user', () => {
  const id = ref<number | undefined>(undefined);
  const username = ref('');
  const email = ref('');
  const date_joined = ref('');
  const isAuthenticated = ref(false);
  const is_staff = ref(false);
  const is_superuser = ref(false);
  const permissions = ref<string[]>([]);
  const roles = ref<any[]>([]);

  function setUserInfo(userInfo: Partial<UserState>) {
    if (userInfo.id !== undefined) id.value = userInfo.id;
    if (userInfo.username !== undefined) username.value = userInfo.username;
    if (userInfo.email !== undefined) email.value = userInfo.email;
    if (userInfo.date_joined !== undefined) date_joined.value = userInfo.date_joined;
    if (userInfo.isAuthenticated !== undefined) isAuthenticated.value = userInfo.isAuthenticated;
    if (userInfo.is_staff !== undefined) is_staff.value = userInfo.is_staff;
    if (userInfo.is_superuser !== undefined) is_superuser.value = userInfo.is_superuser;
    if (userInfo.permissions !== undefined) permissions.value = userInfo.permissions;
    if (userInfo.roles !== undefined) roles.value = userInfo.roles;

    // 从角色中提取权限
    if (userInfo.roles) {
      
      // 获取完整的角色信息
      // api.get('/polls/api/roles/').then(response => {
      //   const allRoles = response.data;
      //   // 找出用户拥有的角色
      //   const userRoles = allRoles.filter((role: any) => 
      //     userInfo.roles?.some((userRole: any) => 
      //       (typeof userRole === 'object' ? userRole.id : userRole) === role.id
      //     )
      //   );
        console.log(userInfo.permissions)
        // 从权限数组中提取codename
        const userPermissions = userInfo.permissions?.map((permission: any) => permission.codename);
        permissions.value = Array.from(new Set(userPermissions));
      // }).catch(error => {
      //   console.error('获取角色信息失败:', error);
      // });
    }
    console.log(permissions.value)
    // 保存用户信息到localStorage
    localStorage.setItem(
      'userInfo',
      JSON.stringify({
        id: id.value,
        username: username.value,
        email: email.value,
        date_joined: date_joined.value,
        isAuthenticated: isAuthenticated.value,
        is_staff: is_staff.value,
        is_superuser: is_superuser.value,
        permissions: permissions.value,
        roles: roles.value,
      })
    );
  }

  function clearUserInfo() {
    id.value = undefined;
    username.value = '';
    email.value = '';
    date_joined.value = '';
    isAuthenticated.value = false;
    is_staff.value = false;
    is_superuser.value = false;
    permissions.value = [];
    roles.value = [];
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
          // 先获取用户信息
          const userData = await import('@/api/user').then(m => m.getCurrentUser());
          
          // 先设置基本用户信息
          setUserInfo({
            ...userData,
            isAuthenticated: true,
          });
          console.log('获取到的角色:', userData.roles);
          // 确保用户有角色信息后再获取权限
          if (userData.roles && userData.roles.length > 0) {
            
            try {
              // 将角色ID数组转换为逗号分隔的字符串
              const roleIds = userData.roles.map((role: any) => 
                typeof role === 'object' ? role.id : role
              ).join(',');
              
              // 根据角色ID获取权限
              const permissions = await import('@/api/user').then(m => m.getPermissionsByRoleIds(roleIds));
              
              console.log('获取到的权限:', permissions);
              
              // 更新用户权限信息
              setUserInfo({
                ...userData,
                isAuthenticated: true,
                permissions: permissions,
              });
            } catch (permError) {
              console.error('获取用户权限失败:', permError);
              // 权限获取失败不影响用户基本信息
            }
          }
        } catch (error) {
          console.error('获取用户信息失败:', error);
          clearUserInfo();
        }
      }
    }
  }

  return {
    id,
    username,
    email,
    date_joined,
    isAuthenticated,
    is_staff,
    is_superuser,
    setUserInfo,
    clearUserInfo,
    initUserInfo,
    permissions,
    roles,
  };
});
