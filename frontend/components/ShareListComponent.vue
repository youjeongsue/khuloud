<template>
  <v-layout justify-center="center" class="my-5">
    <v-flex
      xs12 md10>
      <v-container>
        <v-row dense>
          <v-col
            v-for="(item, i) in shareFolders"
            :key="i"
            cols="15"
          >
            <v-card
              outlined
              height="180"
            >
              <v-card-text>
                <v-card-title
                  class="headline"
                  v-text="item.name"
                ></v-card-title>
                <v-card-text class="caption">{{ item.owner}} 가 공유함</v-card-text>
                <v-card-actions>
                  <v-spacer/>
                  <v-btn
                    text
                    color="blue darken-3"
                    :to="item.id"
                    calss="caption"
                    @click="goToShareFolder(item)"
                  >이동
                  </v-btn>
                  <v-btn
                    text
                    color="blue darken-3"
                    @click="deleteShareFolder(item)"
                    calss="caption"
                  >삭제
                  </v-btn>
                </v-card-actions>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-flex>
  </v-layout>
</template>

<script>
  import ShareNavbarComponent from "../components/ShareNavbarComponent";

  export default {
    components: {ShareNavbarComponent},
    data() {
      return {}
    },
    computed: {
      shareFolders() {
        return this.$store.state.file.shareFolders
      }
    },
    methods: {
      async deleteShareFolder(item) {
        confirm('정말로 삭제하시겠습니까?');
        await this.$store.dispatch('file/deleteShareFolder', {
          id: item.id
        })
      },
      goToShareFolder(item) {
        return this.$router.push(`/drive/shared-with-me?id=${item.id}`);
      }
    },
    async created() {
      try {
        await this.$store.dispatch('file/loadShareFolder')
      } catch (e) {
        console.error(e);
      }
    }
  }
</script>
