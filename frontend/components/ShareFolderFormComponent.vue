<template>
  <v-dialog
    v-model="dialog"
    max-width="500px">
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
        <v-icon outlined>mdi-account-multiple-plus-outline</v-icon>
        <span class="headline-6 pl-4">공유 폴더</span>
      </v-card-title>
      <v-form class="px-3" @submit.prevent="createShareFolder">
        <v-card-text>
          <v-text-field
            filled
            label="폴더 이름"
            v-model="name"
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
            @click="dialog = false">
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
      shareFolders() {
        return this.$store.state.file.shareFolders
      }
    },
    data() {
      return {
        valid: false,
        name: '',
        dialog: false,
      }
    },
    methods: {
      async createShareFolder() {
        try {
          await this.$store.dispatch('file/createShareFolder', {
              name: this.name,
              owner: this.me.username
          });
          this.name = ''
        } catch (e) {
          console.error(e);
        }
      },

    },

  }
</script>

<style scoped>

</style>
