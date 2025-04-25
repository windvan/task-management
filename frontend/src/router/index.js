import { createRouter, createWebHistory } from 'vue-router'

import MessageView from '../views/messages/MessageView.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import MainLayout from '../layouts/MainLayout.vue'
import TasksView from '@/views/tasks/TasksView.vue'
import IconsView from '@/views/others/IconsView.vue'
import ProjectsView from '@/views/projects/ProjectsView.vue'
import ProductsView from '@/views/products/ProductsView.vue'
import SamplesView from '@/views/samples/SamplesView.vue'
import CROsView from '@/views/cros/CROsView.vue'
import UsersView from '@/views/users/UsersView.vue'
import LinksView from '@/views/others/LinksView.vue'
import NotificationCenter from '@/components/NotificationCenter.vue'
  
  
const roleRoutes = {
  Admin: [
    'Dashboard',
    'Products',
    'Projects',
    'Tasks',
    'CROs',
    'Samples',
    'Users',
    'Setting',
    'Icons'
  ],
  Operation: [
    
    'Tasks',
    'CROs',
    'Setting'
  ],
  Portfolio: [
    'Products',
    'Projects',
    'Tasks',
    'Samples',
    'Dashboard',
    'Setting'
  ],
  Science_Delivery: [
    'Tasks',
    'CROs',
    'Users',
    'Samples',
    'Dashboard',
  ]
  ,
  Guest: [
    'Dashboard',
  ]
}

import { useAuthStore } from '../stores/authStore'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: MainLayout,
      redirect: '/dashboard',
      meta: { requiresAuth: true },
      children: [
        
        {
          path: 'dashboard',
          component: DashboardView,
          meta: { requiresAuth: true }
        },
        {
          path: 'products',
          component: ProductsView,
          meta: { requiresAuth: true }
        },
        {
          path: 'projects',
          component: ProjectsView,
          meta: { requiresAuth: true }
        },
        {
          path: 'tasks',
          component: TasksView,
          meta: { requiresAuth: true }
        },
        {
          path: 'cros',
          component: CROsView,
          meta: { requiresAuth: true }
        },
        {
          path: 'samples',
          component: SamplesView,
          meta: { requiresAuth: true }
        },
        {
          path: 'users',
          component: UsersView,
          meta: { requiresAuth: true }
        },
        {
          path: '/setting',
          meta: { requiresAuth: true },
          component: () => import('@/views/others/SysSetting.vue')
        },
        {
          path: 'icons',
          component: IconsView,
          meta: { requiresAuth: true }
        },
        {
          path: 'links',
          component: LinksView,
          meta: { requiresAuth: true }
        },
        {
          path: 'test',
          component: () => import('@/views/others/TestView.vue'),
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/message',
      component: MessageView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginView.vue')
    },

    {
      path: '/:pathMatch(.*)*',
      component: () => import('@/views/auth/404NotFound.vue')
    }
  ]
})



router.beforeEach(async (to, from, next) => {
  // 刷新页面，会触发登陆状态验证（auth/check）
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const authStore = useAuthStore()

  if (requiresAuth) {
    // 如果需要授权，先检查登录状态
    if (authStore.isLoggedIn) {
      // 已登录，正常跳转
      next()
    } else {
      // 未登录，调用 checkAuthStatus() 更新登录状态
      await authStore.checkAuthStatus()

      if (authStore.isLoggedIn) {
        // 更新状态成功，直接跳转
        next()
      } else {
        // 更新状态失败，跳转到登录
        next({ path: '/login', query: { redirect: to.fullPath } })
      }
    }
  } else {
    // 不需要授权，直接跳转
    next()
  }
})

export default router
export { roleRoutes }
