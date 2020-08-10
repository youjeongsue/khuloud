<template>
  <v-dialog
    v-model="dialog"
    max-width="400px">
    <template v-slot:activator="{on}">
      <v-btn
        flat slot="activator"
        text
        v-on="on">
        <v-icon>add</v-icon>
        <span overline class="caption">새로 만들기</span>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <v-icon outlined>mdi-folder-plus-outline</v-icon>
        <span class="headline-6 pl-4">폴더</span>
      </v-card-title>
      <v-form class="px-3" @submit.prevent="uploadFolder">
        <v-card-text>
          <v-text-field
            outlined
            label="폴더 이름"
            v-model="folderName"
            color="blue"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            depressed
            class="mr-3 mb-3 caption"
            type="submit"
            color="blue darken-3"
            dark
            @click="dialog = false"
          >
            만들기
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
  import moment from 'moment';

  export default {
    name: "CreateFolderFormComponent",
    computed: {
      me() {
        return this.$store.state.user.me;
      },
      currentFolder() {
        return this.$store.state.file.currentFolder
      }
    },
    data() {
      return {
        valid: false,
        folderName: '',
        dialog: false,
      }
    },
    methods: {
      folderPath(){
        return this.currentFolder.path + this.folderName + '/'
      },
      async uploadFolder() {
        try {
          var now = Date.now();
          now = moment(now).format("YYYY-MM-DD");
          const formData = new FormData();
          formData.append('name', this.folderName);
          formData.append('owner', this.me.username);
          formData.append('path', this.folderPath());
          formData.append('isFolder', true);
          // formData.append('createdDate', now);
          formData.append('modifiedDate', now);
          formData.append('filesize', 0);
          formData.append('share', false);
          formData.append('cid', this.currentFolder.id);

          console.log("TEST", now, this.folderPath, this.folderName);
          this.dialog = false;
          await this.$store.dispatch('file/uploadFolder', {formData});
          this.folderName = '';
        } catch (e) {
          console.error(e);
        }
      },

    }
  }
</script>

<style scoped>

</style>
