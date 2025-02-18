<template>
  <div class="mx-auto mt-24 p-4 max-w-80 card  bg-white">
    <h2 class="mb-8 text-center text-primary font-bold text-xl">Login</h2>
    <Form :resolver @submit="handleLogin" pt:root="flex flex-col gap-8 mb-6">
      <FormField v-slot="$field" name="username">
        <FloatLabel>
          <InputText id="email" pt:root:autocomplete="email" fluid></InputText>
          <label for="email">Email</label>
        </FloatLabel>
        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{ $field.error?.message }}
        </Message>
      </FormField>

      <FormField v-slot="$field" name="password">
        <FloatLabel>
          <Password inputId="password" :feedback="false" fluid toggleMask
            pt:pcInputText:root:autocomplete="current-password"></Password>
          <label for="password">Password</label>
        </FloatLabel>
        <Message v-if="$field?.invalid" severity="error" size="small" variant="simple">{{ $field.error?.message }}
        </Message>
      </FormField>
      <Button label="Login" type="submit" rounded size="small" class="mx-8" />
      <Button label="SSO" @click="handleSSOLogin" rounded size="small" class="mx-8" severity="secondary"></Button>
    </Form>
    <Message severity="error" v-if="loginErrorMessage">
      {{ loginErrorMessage }}
    </Message>
  </div>
</template>

<script setup name="LoginView">

  import { useAuthStore } from '@/stores/authStore';
  import { storeToRefs } from 'pinia'
  import { yupResolver } from '@primevue/forms/resolvers/yup'
  import * as yup from 'yup'


  const authStore = useAuthStore();
  const { login } = authStore;
  const { loginErrorMessage } = storeToRefs(authStore);

  const resolver = yupResolver(yup.object().shape({
    username: yup.string().email("Invalid email address!").required("Email is required!"),
    password: yup.string().required("Password is required!"),
  }))


  function handleLogin(e) {
    if (e.valid) {
      login(e.values,,)
    }
  }

  const handleSSOLogin = () => {
    // 实现SSO登录逻辑
    console.log('SSO登录')
  }
</script>
