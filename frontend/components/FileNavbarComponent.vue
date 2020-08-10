<template>
  <v-system-bar
    :height="55">

    <create-folder-form-component/>

    <create-file-form-component/>
    <v-spacer></v-spacer>
    <v-menu offset-y>
      <template
        v-slot:activator="{on}">
        <v-btn
          text
          v-on="on"
        >
          <v-icon>sort</v-icon>
          <span class="caption">정렬</span>
        </v-btn>
      </template>
      <v-list>
        <v-list-item v-for="view in views" :key="view.title" @click="changeCurrentView(view.title)">
          <v-list-action>
            <v-icon small>{{view.icon}}</v-icon>
          </v-list-action>
          <v-list-title class="ml-1 body-2">{{view.title}}</v-list-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-system-bar>
</template>

<script>
  import 'material-design-icons-iconfont/dist/material-design-icons.css'
  import CreateFolderFormComponent from "./CreateFolderFormComponent";
  import CreateFileFormComponent from "./CreateFileFormComponent";

  export default {
    name: "FileNavbarComponent",
    components: {CreateFolderFormComponent, CreateFileFormComponent},
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
