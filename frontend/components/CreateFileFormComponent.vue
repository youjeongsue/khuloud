<template>
  <div>
    <v-btn
      text
      @click="$refs.fileInput.click()">
      <v-icon>vertical_align_top</v-icon>
      <span class="caption">업로드</span>
    </v-btn>
    <input
      v-show="false"
      type="file"
      ref="fileInput"
      multiple="multiple"
      @change="uploadFile">
  </div>
</template>

<script>
  import 'material-design-icons-iconfont/dist/material-design-icons.css'
  import moment from 'moment';

  export default {
    name: "CreateFileFormComponent",
    computed: {
      currentFolder() {
        return this.$store.state.file.currentFolder
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
      async uploadFile(e) {
        try {
          const formData = new FormData();
          var now = Date.now();
          now = moment(now).format('YYYY-MM-DD');
          Array.prototype.forEach.call(e.target.files, (file) => {
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
      }
    }
  }
</script>

<style scoped>

</style>
