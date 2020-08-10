<!--async createStarFile() {-->
<!--try {-->
<!--var id = [];-->
<!--for (var i = 0; i < this.selected.length; i++) {-->
<!--if (this.selected[i].isFolder === false) {-->
<!--id.push(this.selected[i].id);-->
<!--}-->
<!--}-->
<!--await this.$store.dispatch('file/createStarFile', {id: id});-->

<!--} catch (e) {-->
<!--console.error(e);-->
<!--}-->
<!--}-->


<template>
  <v-layout justify-center="center" class="my-10">
    <v-flex
      xs12 md10>
      <v-card elevation="0">
        <v-card-title class="font-weight-bold">
          내 드라이브
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

            <!-- rename dialog-->
            <v-dialog v-model="edit_dialog" max-width="500px">
              <v-card>
                <v-card-title>
                  <v-icon>mdi-pencil-outline</v-icon>
                  <span class="headline-6 pl-4">파일 이름 변경</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col md="20">
                        <v-text-field filled v-model="newname" label="변경할 이름을 입력하세요."></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-3" flat @click="renameFile" class="caption" dark>수정</v-btn>
                  <v-btn color="blue darken-3" flat @click.native="edit_dialog = false" class="caption" dark>닫기</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <!--            -->

            <!--share dialog-->
            <v-dialog v-model="share_dialog" persistent max-width="500px">
              <v-card>
                <v-card-title>
                  <v-icon outlined>mdi-account-multiple-plus-outline</v-icon>
                  <span class="headline-6 pl-4">사용자 및 그룹과 공유</span>
                </v-card-title>
                <v-card-text>
                  <v-list subheader>
                    <v-subheader>공유문서함</v-subheader>

                    <v-list-item
                      v-for="item in shareFolders"
                      :key="item.name"
                      @click="createShareFile(item)"
                    >
                      <v-list-item-avatar icon>
                        <v-icon>folder</v-icon>
                      </v-list-item-avatar>

                      <v-list-item-content>
                        <v-list-item-title v-text="item.name"></v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>

                <v-card-actions>
                  <v-spacer/>
                  <v-btn color="blue darken-3" flat @click="share_dialog = false" class="caption" dark>닫기</v-btn>
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
            <v-list dense>
              <v-list-item @click="downloadItem">
                <v-list-item-title class="body-2">다운로드</v-list-item-title>
              </v-list-item>
              <v-list-item @click="deleteItem">
                <v-list-item-title class="body-2">삭제</v-list-item-title>
              </v-list-item>
              <v-list-item @click="editItem">
                <v-list-item-title class="body-2">이름 바꾸기</v-list-item-title>
              </v-list-item>
              <v-divider
                class="mx-4"
                :inset="inset"
              ></v-divider>
              <v-list-item @click="createStarFile">
                <v-list-item-title class="body-2">중요문서함에 추가</v-list-item-title>
              </v-list-item>
              <v-list-item @click="shareItem">
                <v-list-item-title class="body-2">공유하기</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          <v-spacer/>
          <!--          검색-->
          <v-text-field
            v-model="search"
            prepend-inner-icon="mdi-magnify"
            class="caption"
            label="검색"
            single-line
            hide-details
            outlined
            clearable
            dense
          ></v-text-field>
          <!--          -->
        </v-card-title>


        <v-card
          elevation="0"
          @dragover.prevent
          @dragenter.prevent
          @drop.prevent="onDrop"
        >
          <!--        데이터테이블 -->
          <v-data-table
            v-model="selected"
            :headers="headers"
            :items="files"
            :search="search"
            class="elevation-0"
            show-select
            @click:row="loadFiles"
            hide-default-footer
          >

            <template v-slot:item.type="{item}">
              <v-icon>{{ extension_to_icon(item)}}</v-icon>
            </template>
          </v-data-table>
          <!--        <div class="text-center">-->
          <!--          <v-pagination-->
          <!--            v-model="page"-->
          <!--            :length="3"-->
          <!--            circle-->
          <!--            prev-icon="mdi-menu-left"-->
          <!--            next-icon="mdi-menu-right"-->
          <!--          ></v-pagination>-->
          <!--        </div>-->
        </v-card>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  import 'material-design-icons-iconfont/dist/material-design-icons.css'
  import moment from "moment";

  export default {
    computed: {
      files() {
        return this.$store.state.file.files
      },
      currentFolder() {
        return this.$store.state.file.currentFolder
      },
      fileUrl() {
        return this.$store.state.file.fileUrl
      },
      me() {
        return this.$store.state.user.me
      },
      shareFolders() {
        return this.$store.state.file.shareFolders
      },
      fileUrl() {
        return this.$store.state.file.fileUrl
      }
    },
    data() {
      return {
        showShareFolderList: false,
        page: 1,
        edit_dialog: false,
        share_dialog: false,
        preview_dialog: false,
        download_dialog: false,
        selected: [],
        search: '',
        editedIndex: -1,
        newname: '',
        oldname: '',
        headers: [
          {text: '타입', value: 'type', width: '50px'},
          {text: '이름', sortable: 'false', value: 'name', width: '150px'},
          {text: '수정한 날짜', value: 'modifiedDate', width: '100px'},
          {text: '파일 크기', value: 'filesize', width: '100px'},
        ],
      }
    },
    methods: {
      folderpath() {
        return this.currentFolder.path;
      },
      changeFileSize(byteSize) {
        var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        if (byteSize === 0) return '-';
        var i = parseInt(Math.floor(Math.log(byteSize) / Math.log(1024)));
        return Math.round(byteSize / Math.pow(1024, i), 2) + ' ' + sizes[i];
      },
      loadFiles(value) {
        if (value.isFolder === true) {
          console.log('file', value.id);
          return this.$router.push(`/drive/file?cid=${value.id}&&owner=${this.me.username}`);
        }
      },
      async shareItem(item) {
        try {
          this.share_dialog = true;
          await this.$store.dispatch('file/loadShareFolder');
        } catch (e) {
          console.error(e);
        }
      },
      async deleteItem() {
        try {
          var id = [];
          var path = [];
          var name = [];
          for (var i = 0; i < this.selected.length; i++) {
            id.push(this.selected[i].id);
            path.push(this.selected[i].path);
            name.push(this.selected[i].name);
          }
          if (confirm('정말로 삭제하시겠습니까?') === true) {
            await this.$store.dispatch('file/deleteFile', {id: id, path: path});
          }
        } catch (e) {
          console.error(e);
        }
      },
      async onDrop(e) {
        try {
          const formData = new FormData();
          var now = Date.now();
          now = moment(now).format('YYYY-MM-DD');
          Array.prototype.forEach.call(e.dataTransfer.files, (file) => {
            formData.append('file', file);
            formData.append('name', file.name);
            formData.append('isFolder', false);
            formData.append('path', this.folderpath() + file.name);
            formData.append('filesize', this.changeFileSize(file.size));
            // formData.append('createdDate', now);
            formData.append('modifiedDate', now);
            formData.append('share', false);
            formData.append('cid', this.currentFolder.id);
            console.log(file);
            console.log(this.changeFileSize(file.size))
          });

          await this.$store.dispatch('file/uploadFiles', {formData});
          // return this.$router.replace('/');
        } catch (e) {
          console.error(e);
        }
      },
      editItem(item) {
        const index = this.selected.indexOf(item);
        this.edit_dialog = true;
      },
      previewItem(item) {
        this.preview_dialog = true;
      },
      async renameFile() {
        try {
          var id = this.selected[0].id;
          await this.$store.dispatch('file/renameFile', {id: id, newname: this.newname})
          this.edit_dialog = false;
        } catch (e) {
          console.error(e);
        }
      },
      async createStarFile() {
        try {
          var id = [];
          for (var i = 0; i < this.selected.length; i++) {
            if (this.selected[i].isFolder === false) {
              id.push(this.selected[i].id);
            }
          }
          await this.$store.dispatch('file/createStarFile', {id: id});
          this.selected = []
        } catch (e) {
          console.error(e);
        }
      },
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
      async createShareFile(item) {
        try {
          var id = item.id;
          var fileId = [];
          for (var i = 0; i < this.selected.length; i++) {
            if (this.selected[i].isFolder === false) {
              fileId.push(this.selected[i].id);
            }
          }
          console.log(id, fileId);
          await this.$store.dispatch('file/createShareFile', {id: id, fileId: fileId});
          this.share_dialog = false
        } catch (e) {
          console.error(e);
        }
      },
      extension_to_icon(item) {
        const name = item.name;
        const isFolder = item.isFolder;
        const extension = name.split('.').pop();
        if (isFolder === true) {
          return 'mdi-folder';
        } else if (extension === 'png'
          || extension === 'jpg'
          || extension === 'gif'
          || extension === 'jpeg'
          || extension === 'ai'
        ) {
          return 'mdi-file-image'
        } else if (extension === 'mp4'
          || extension === 'mov'
          || extension === 'avi'
          || extension === 'mpg'
          || extension === 'asf'
        ) {
          return 'mdi-file-video'
        } else if (extension === 'hwp'
        ) {
          return 'mdi-file-document'
        } else if (extension === 'doc'
          || extension === 'docx'
          || extension === 'docm'
          || extension === 'dotx'
          || extension === 'dotm'
        ) {
          return 'mdi-file-word'
        } else if (extension === 'pdf'
        ) {
          return 'mdi-file-pdf'
        } else if (extension === 'pptx'
          || extension === 'pot'
          || extension === 'ppsx'
          || extension === 'pps'
        ) {
          return 'mdi-file-powerpoint'
        } else if (extension === 'xlsx'
          || extension === 'xlsm'
          || extension === 'xlsb'
          || extension === 'xls'
          || extension === 'xml'
        ) {
          return 'mdi-file-powerpoint'
        }
        return 'mdi-file'
      },

    },

  }
</script>
