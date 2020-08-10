<template>
  <v-navigation-drawer v-model="drawer" clipped app>
    <v-list>
      <v-list-item-group v-model="item">
        <v-list-item v-for="(item, i) in items" :key="i" :to="item.route">
          <v-list-item-icon>
            <v-icon v-text="item.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="item.title"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
  import 'material-design-icons-iconfont/dist/material-design-icons.css'

  export default {
    name: 'LeftNavbarComponent',
    components: {
      me(){
        return this.$store.state.user.me
      }

    },
    data() {
      return {
        drawer: null,
        item: 1,
        items: [
          {title: '내 드라이브', icon: 'folder_open', route: `/drive/file?cid=0`},
          {title: '최근 문서함', icon: 'schedule', route: '/drive/recent'},
          {title: '공유 문서함', icon: 'people_outline', route: '/drive/shared-with-me-index'},
          {title: '중요 문서함', icon: 'star_outline', route: '/drive/starred'},
          {title: '휴지통', icon: 'delete_outline', route: '/drive/trash'},
          {title: '계정', icon: 'portrait', route: '/myaccount'},
        ]
      }
    },
  }
</script>
