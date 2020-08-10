<template>
  <v-layout row justify-center>
    <v-dialog v-model="dialog" persistent max-width="500px">
      <template v-slot:activator="{on}">
        <v-btn
          flat slot="activator"
          text
          v-on="on">
          <v-icon>add</v-icon>
          <span overline class="caption">공유하기</span>
        </v-btn>
      </template>

      <v-form class="px-3" @submit.prevent="createShareUser">
        <v-card>
          <v-card-title>
            <v-icon outlined>person_add</v-icon>
            <span class="headline-large-weight pl-4">사용자 및 그룹과 공유</span>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout row wrap>
                <v-flex xs20 sm20 md20>
                  <v-text-field filled v-model="username" box label="사용자 및 그룹 추가" class="caption"></v-text-field>
                  <small>*추가할 사용자의 아이디를 입력하세요.</small>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn type="submit" color="blue darken-3" flat @click="dialog = false" class="caption" dark>공유</v-btn>
            <v-btn color="blue darken-3" flat @click="dialog = false" class="caption" dark>닫기</v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>
  </v-layout>
</template>
<script>
  import 'material-design-icons-iconfont/dist/material-design-icons.css'

  export default {
    name: "ShareFormComponent",
    data() {
      return {
        dialog: false,
        username: ''
      }
    },
    computed: {
      shareFolder() {
        return this.$store.state.file.shareFolder
      }
    },
    methods: {
      async createShareUser() {
        try {
          await this.$store.dispatch('file/createShareUser', {
            id: this.shareFolder.id,
            username: this.username
          })
        } catch (e) {
          console.error(e);
        }
      }
    }
  }
</script>
