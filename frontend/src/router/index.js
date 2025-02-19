import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
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

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const { isLoggedIn } = useAuthStore()
  if (requiresAuth && !isLoggedIn) {
    next({ path: '/login' })
  } else {
    next()
  }
})

export default router
