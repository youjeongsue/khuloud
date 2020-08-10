<template>
  <v-layout justify-center="center" class="my-10">
    <v-flex xs12 md10>
      <v-card elevation="0">
        <v-card-title class="font-weight-bold">중요문서함
          <v-menu
            :close-on-content-click="false"
            :nudge-width="200"
            offset-x
            min-width="200">
            <template v-slot:activator="{ on }">
              <v-btn
                dark
                v-on="on"
                elevation="class-0"
                color="blue darken-3"
                class="ma-2"
                small
                tile
              >메뉴
              </v-btn>
            </template>
            <v-list dense>
              <v-list-item @click="downloadItem">
                <v-list-item-title class="body-2">다운로드</v-list-item-title>
              </v-list-item>
              <v-list-item @click="deleteStarFile">
                <v-list-item-title class="body-2">중요문서함에서 삭제</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-card-title>

        <v-data-table
          v-model="selected"
          :headers="headers"
          :items="files"
          hide-actions show-select hide-default-footer>
          <template v-slot:item.type="{item}">
            <div v-if="item.isFolder">
              <v-btn icon>
                <v-icon color="yellow darken-2">folder</v-icon>
              </v-btn>
            </div>
            <div v-else>
              <v-btn icon>
                <v-icon color="blue darken-2">description</v-icon>
              </v-btn>
            </div>
          </template>
        </v-data-table>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  import 'material-design-icons-iconfont/dist/material-design-icons.css'
  import moment from 'moment';

  export default {
    name: 'StarTableComponent',
    data() {
      return {
        selected: [],
        headers: [
          {
            text: '타입',
            value: 'type',
          },
          {
            text: '이름',
            align: 'left',
            sortable: 'false',
            value: 'name'
          },
          {text: '소유자', value: 'owner'},
          {text: '최종 수정 날짜', value: 'modifiedDate'},
          {text: '크기', value: 'filesize'}
        ],
      }
    },
    computed: {
      files() {
        return this.$store.state.file.files
      }
    },
    methods: {
      async downloadItem() {
        try {
          var id = [];
          var path = [];
          var name = [];
          for (var i = 0; i < this.selected.length; i++) {
            if (this.selected[i].isFolder === false) {
              id.push(this.selected[i].id);
              path.push(this.selected[i].path);
              name.push(this.selected[i].name);
            }
          }
          await this.$store.dispatch('file/downloadFile', {id: id, path: path});

        } catch (e) {
          console.error(e);
        }
      },
      async deleteStarFile() {
        try {
          var id = [];

          for (var i = 0; i < this.selected.length; i++) {
            id.push(this.selected[i].id);
          }
          if (confirm('정말로 중요문서함 삭제하시겠습니까?') === true) {
            await this.$store.dispatch('file/deleteStarFile', {id: id});
          }
          this.selected = []
        } catch (e) {
          console.error(e);
        }
      }
    }
  }
</script>
