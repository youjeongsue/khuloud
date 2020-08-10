<template>
  <v-system-bar
    :height="55">
    <share-folder-form-component/>
  </v-system-bar>
</template>

<script>
  import 'material-design-icons-iconfont/dist/material-design-icons.css'
  import ShareFolderFormComponent from "./ShareFolderFormComponent";

  export default {
    name: "ShareNavbarComponent",
    components: {ShareFolderFormComponent},
    data() {
      return {
        currentView: 0,
        views: [
          {value: 0, icon: 'format_align_left', title: '목록'},
          {value: 1, icon: 'border_all', title: '타일'}
        ],
      }
    },
    methods: {
      changeCurrentView(value) {
        this.currentView = value;
        console.log(this.currentView);
      },
    }
  }
</script>

<style scoped>
</style>
