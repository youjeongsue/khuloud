<template>
  <v-layout justify-center="center" class="my-10">
    <v-flex xs12 md10>
      <v-card elevation="0">
        <v-card-title class="font-weight-bold">공유 문서함
          <v-menu
            :close-on-content-click="false"
            :nudge-width="200"
            offset-x
            min-width="200">

            <!--            download dialog-->
            <v-dialog v-model="download_dialog" max-width="500px">
              <v-card>
                <v-card-title>
                  <v-icon>mdi-cloud-download-outline</v-icon>
                  <span class="headline-6 pl-4">다운로드</span>
                </v-card-title>
                <v-card-text align="center" justify="center">
                  <v-btn @click="$refs.download.click()" icon class="mr-3 justify-center" color="secondary icon">
                    <v-icon x-large>mdi-folder</v-icon>
                    <a ref="download" :href="fileUrl" :download="fileUrl" style="color: #ffffff"></a>
                  </v-btn>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-3" flat @click.native="download_dialog = false" class="caption" dark>닫기
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <!--            -->


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
              <v-list-item @click="downloadItem">
                <v-list-item-title class="body-2">다운로드</v-list-item-title>
              </v-list-item>
              <v-list-item @click="deleteShareFile">
                <v-list-item-title class="body-2">공유문서함에서 삭제</v-list-item-title>
              </v-list-item>
              <v-divider/>
              <v-list-item @click="deleteShareUser">
                <v-list-item-title class="body-2">멤버 삭제</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-card-title>


        <!--        공유문서함 멤버 목록-->
        <v-card
          outlined
          width="300px"
        >
          <v-list>
            <v-subheader class="">멤버</v-subheader>
            <v-list-item-group color="primary" v-model="settings">
              <v-list-item
                v-for="(item, i) in shareUsers"
                :key="i"
              >
                <template v-slot:default="{active, toggle}">
                  <v-list-item-icon>
                    <v-icon small>mdi-account</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title v-text="item.username"></v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-checkbox
                      v-model="active"
                      @click="toggle"
                    >
                    </v-checkbox>
                  </v-list-item-action>
                </template>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card>

        <!--        -->


        <v-data-table
          v-model="selected"
          :headers="headers"
          :items="shareFiles"
          hide-actions
          show-select
          hide-default-footer
        >
          <template v-slot:item.updated_at="{item}">
            <div>{{$moment(item.updated_at).format('YYYY-MM-DD')}}</div>
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
    name: 'ShareTableComponent',
    data() {
      return {
        selected: [],
        settings: [],
        members: [],
        headers: [
          {text: '타입', value: 'type', width: '10px', align: 'center'},
          {text: '이름', sortable: 'false', value: 'name', width: '150px', align: 'left'},
          {text: '공유된 날짜', value: 'updated_at', width: '100px', align: 'center'},
          {text: '공유한 사람', value: 'owner', width: '100px', align: 'center'},
          {text: '공유', value: 'share', width: '100px', align: 'center'}
        ],
        download_dialog: false,
      }
    },
    computed: {
      shareUsers() {
        return this.$store.state.file.shareUsers
      },
      shareFiles() {
        return this.$store.state.file.shareFiles
      },
      shareFolder() {
        return this.$store.state.file.shareFolder
      },
      fileUrl() {
        return this.$store.state.file.fileUrl
      }
    },
    methods: {
      async downloadItem() {
        try {
          this.download_dialog = true;
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
      async deleteShareFile() {
        try {
          var id = this.shareFolder.id;
          var fileId = [];
          for (var i = 0; i < this.selected.length; i++) {
            fileId.push(this.selected[i].id);
          }
          if (confirm('정말로 삭제하시겠습니까?') === true) {
            await this.$store.dispatch('file/deleteShareFile', {
              id: this.shareFolder.id,
              fileId: fileId
            })
          }

        } catch (e) {
          console.error(e);
        }
      },
      async deleteShareUser() {
        try {
          if (confirm('정말로 삭제하시겠습니까?') === true) {
            await this.$store.dispatch('file/deleteShareUser', {
              id: this.shareFolder.id,
              userId: this.shareUsers[this.settings].id
            });
          }
        } catch (e) {
          console.error(e);
        }
      }


    },
  }
</script>
