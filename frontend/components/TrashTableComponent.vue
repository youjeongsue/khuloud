<template>
  <v-layout justify-center="center" class="my-10">
    <v-flex xs12 md10>
      <v-card elevation="0">
        <v-card-title class="font-weight-bold">
          휴지통
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
            <v-list dense shaped>
              <v-list-item  @click="restoreFile">
                <v-list-item-title class="body-2">복원</v-list-item-title>
              </v-list-item>
              <v-list-item  @click="hardDelete">
                <v-list-item-title class="body-2">영구 삭제</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-card-title>

        <v-data-table
          v-model="selected"
          :headers="headers"
          :items="files"
          hide-actions
          show-select
          hide-default-footer
        >
          <template v-slot:item.deleted_at="{item}">
            <div>{{$moment(item.deleted_at).format('YYYY-MM-DD')}}</div>
          </template>

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
  export default {
    name: 'TrashTableComponent',
    data () {
      return {
        selected: [],
        headers: [
          { text: '타입', value: 'type', width: '30px'},
          { text: '이름', sortable: 'false', value: 'name', width: '150px',align: 'left'},
          { text: '삭제된 날짜', value: 'deleted_at', width: '100px',align: 'center'},
          { text: '만든 사람', value: 'owner', width: '100px',align: 'center'},
          { text: '원래 위치', value:'path', width: '100px',align: 'center'}
        ],
      }
    },
    computed: {
      files() {
        return this.$store.state.file.files
      }
    },
    methods: {
      async restoreFile() {
        try {
          var id = [];

          for (var i = 0; i < this.selected.length; i++) {
            id.push(this.selected[i].id);
          }
          if (confirm('정말로 복원하시겠습니까?') === true) {
            await this.$store.dispatch('file/restoreFile', {id: id});
          }
        } catch (e) {
          console.error(e);
        }
      },
      async hardDelete() {
        try {
          var id = [];
          for (var i = 0; i < this.selected.length; i++) {
            id.push(this.selected[i].id);
          }
          if (confirm('정말로 영구 삭제하시겠습니까?') === true) {
            await this.$store.dispatch('file/hardDelete', {id: id});
          }
        } catch (e) {
          console.error(e);
        }
      },
    }
  }
</script>
<style>

</style>
