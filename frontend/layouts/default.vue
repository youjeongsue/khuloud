<template>
  <v-app>
    <!--    Left Navigation-->
    <LeftNavbarComponent @isDrawer="isDrawer":drawer="drawer"></LeftNavbarComponent>
    <!--    Left Navigation-->

    <!--    app bar-->
    <HeaderComponent/>
    <!--    app bar-->
    <v-content>
      <nuxt/>
    </v-content>

    <!-- Footer -->
    <v-footer fixed app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
    <!-- //Footer -->
  </v-app>
</template>

<script>
  import 'material-design-icons-iconfont/dist/material-design-icons.css'
  import LeftNavbarComponent from "../components/LeftNavbarComponent"
  import HeaderComponent from "../components/HeaderComponent";

  export default {
    name: 'default',
    data: () => ({
      drawer: null
    }),
    props: {
      source: String,
    },
    methods: {
      isDrawer (data){
        this.drawer = data;
      }
    },
    components: {
      HeaderComponent,
      LeftNavbarComponent
    }
  }
</script>
