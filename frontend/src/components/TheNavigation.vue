<template>
  <nav class="flex flex-col flex-none overflow-auto bg-white rounded-md w-52">
    <Menu :model="items"
      :pt="{ root: 'border-none', itemLink: 'p-3', itemContent: 'hover:bg-primary has-[a.isActive]:bg-primary' }">
      <template #item="{ item, props }">
        <router-link v-if="item.route" v-slot="{ href, navigate, isActive }" :to="item.route" custom>
          <a :href="href" v-bind="props.action" @click="navigate" :class="{ isActive: isActive }" aria-hidden="false">
            <span :class="item.icon" />
            <span>{{ item.label }}</span>
          </a>
        </router-link>
        <a v-else :href="item.url" :target="item.target" v-bind="props.action" aria-hidden="false">
          <span :class="item.icon" />
          <span>{{ item.label }}</span>
        </a>
      </template>
    </Menu>

  </nav>
</template>

<script setup>
  import { ref, computed } from 'vue'
  import { useAuthStore } from '../stores/authStore'
  import { roleRoutes } from '../router'

  const authStore = useAuthStore()

  // 定义每个角色可以访问的路由


  // 基础导航项配置
  const baseItems = [

    {
      label: 'Projects',
      icon: 'pi pi-folder',
      route: '/projects'
    },
    {
      label: 'Tasks',
      icon: 'pi pi-list',
      route: '/tasks'
    },
    {
      label: 'Products',
      icon: 'pi pi-bookmark',
      route: '/products'
    },
    {
      label: 'CROs',
      icon: 'pi pi-id-card',
      route: '/cros'
    },
    {
      label: 'Samples',
      icon: 'pi pi-box',
      route: '/samples'
    },
    {
      label: 'Users',
      icon: 'pi pi-users',
      route: '/users'
    },
    {
      separator: true
    },
    {
      label: 'Dashboard',
      icon: 'pi pi-chart-bar',
      route: '/dashboard'
    },
    {
      label: 'Setting',
      icon: 'pi pi-cog',
      route: '/setting'
    },
    {
      label: 'Icons',
      icon: 'pi pi-palette',
      route: '/icons'
    },
    {
      label: 'Links',
      icon: 'pi pi-external-link',
      url: 'https://www.bing.com'
    },
    {
      label: 'testcommand',
      icon: 'pi pi-user',
      command: () => { alert("command test") }
    }, {
      label: 'Test',
      icon: 'pi pi-user',
      route: "/test"
    },
  ]

  // 根据角色过滤导航项
  const items = computed(() => {
    const role = authStore.current_user?.role || 'Guest'
    const allowedRoutes = roleRoutes[role]
    return allowedRoutes
      .map(routeName => baseItems.find(item => item.label === routeName))
      .filter(item => item !== undefined)
  })
</script>

<style module></style>
