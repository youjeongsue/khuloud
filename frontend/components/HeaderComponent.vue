<template>
  <v-app-bar
    app
    clipped-left
    color="blue darken-3"
    dark
  >
    <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
    <v-toolbar-title class="font-weight-light">KHULOUD</v-toolbar-title>
    <v-spacer/>

    <v-btn
      icon
      v-on="on"
      @click="logout"
    >
      <v-icon>exit_to_app</v-icon>
    </v-btn>

  </v-app-bar>
</template>

<script>
  export default {
    name: 'HeaderComponent',
    props: {
      source: String
    },
    methods: {
      async logout() {
        try {
          await  this.$store.dispatch('user/logout');
          await this.$store.commit('file/InitialFiles');
          await  this.$router.replace('/');
        } catch (e) {
          console.error(e);
        }
      },
    }
  }
</script>

<style scoped>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
  }
</style>
