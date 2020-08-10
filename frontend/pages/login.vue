<template>
  <v-layout>
    <v-flex class="text-center">
      <div v-if="me">
        <v-btn @click="logout">로그아웃</v-btn>
      </div>
      <div v-else>
        <div v-if="tryLogin">
          <login-component/>
          <v-btn @click="changeTryLogin">회원가입</v-btn>
        </div>
        <div v-else>
          <sign-up-component/>
          <v-btn @click="changeTryLogin">로그인</v-btn>
        </div>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
import LoginComponent from "../components/LoginComponent"
import SignUpComponent from "../components/SignUpComponent"
import LoginLayout from "../layouts/FormLayout"

export default {
  name: 'login',
  layout: 'FormLayout',
  data() {
    return {
      tryLogin: true,
    }
  },
  computed: {
    me() {
      return this.$store.state.user.me
    }
  },
  components: {
    LoginComponent,
    SignUpComponent,
  },
  methods: {
    changeTryLogin() {
      this.tryLogin = !this.tryLogin
    },
    async logout() {
      try {
        await this.$store.dispatch('user/logout');
        await this.$router.replace('/');
      } catch (e) {
        console.error(e);
      }
    }
  },
}
</script>
