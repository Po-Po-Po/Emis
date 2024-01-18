<template>
  <v-container id="login-form">
    <emis-logo :size=140 :center=true></emis-logo>
    <v-layout style="background-color: #171e2f" align-center justify-center>
      <v-flex>
        <v-card elevation="7">
          <v-card-text>
            <v-form @submit="userLogin">
              <v-text-field
                v-model="login.email"
                label="Login"
                outlined
                @keyup.enter="userLogin"
              ></v-text-field>
              <v-text-field
                v-model="login.password"
                label="Password"
                outlined
                :append-icon="passwordShow ? 'mdi-eye' : 'mdi-eye-off'"
                :type="passwordShow ? 'text' : 'password'"
                @keyup.enter="userLogin"
                @click:append="passwordShow = !passwordShow"
              ></v-text-field>
              <v-btn block color="primary" @click="userLogin">Войти в систему</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex'

export default {
  auth: 'guest',
  name: "LoginForm",
  data: () => ({
    valid: true,
    login: {
      email: '',
      password: '',
      error: ''
    },
    passwordShow: false
  }),
  computed: {
    logging() {
      return this.$store.state.loggingUser
    }
  },
  methods: {
    ...mapMutations({
      loggingIn: 'loggingIn',
    }),
    userLogin() {
      try {
        this.$auth.loginWith('local', { data: this.login }).then(() => {
          this.$toast.success('Успешный вход в систему')
          this.loggingIn()
        })
      } catch (err) {
        this.login.error = "Логине или пароль неверны. Пожалуйста, попробуйте снова.";
        this.$toast.error('Ошибка авторизации')
      }
    }
  }
}
</script>

<style scoped>
#login-form{
  max-width: 500px;
}
</style>
