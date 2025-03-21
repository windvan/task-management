<template>
  <nav class="flex flex-col flex-none overflow-auto bg-white rounded-md w-52">
    <Menu :model="items" :pt="{root:'border-none',itemLink:'p-3',itemContent:'hover:bg-primary has-[a.isActive]:bg-primary'}">
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
  import { ref } from 'vue'


  const items = ref([
    {
      label: 'Dashboard',
      icon: 'pi pi-chart-bar',
      route: '/dashboard'
    },
      {
      label: 'Products',
      icon: 'pi pi-bookmark',
      route: '/products'
    },
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
    },{
      label: 'test',
      icon: 'pi pi-user',
      route:"/test"
    },


  ])


</script>

<style module>


</style>
