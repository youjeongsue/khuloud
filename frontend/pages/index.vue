<template>
  <v-layout>
    <v-flex>
      <div v-if="tryLogin" class="text-center">
        <login-component/>
      </div>
      <div v-else>
        <sign-up-component/>
      </div>
    </v-flex>
  </v-layout>
</template>

<script>
  import FormLayout from "../layouts/FormLayout";
  import LoginComponent from "../components/LoginComponent";
  import SignUpComponent from "../components/SignUpComponent";
  import Login from "./login";
  export default {
    layout: 'FormLayout',
    name: 'index',
    data() {
      return {
        tryLogin: true,
      }
    },
    components: {Login, LoginComponent, SignUpComponent},
  }
</script>

