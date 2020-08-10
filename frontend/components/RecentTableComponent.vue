<template>
  <v-layout justify-center="center" class="my-10">
    <v-flex xs12 md10>
      <v-card elevation="0">
        <v-card-title class="font-weight-bold">최근에 사용한 항목</v-card-title>
        <v-data-table
          v-model="selected"
          :headers="headers"
          :items="files"
          hide-actions
          show-select
          hide-default-footer
        >

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

          <template v-slot:item.updated_at="{item}">
            <div>{{$moment(item.updated_at).format('YYYY-MM-DD')}}</div>
          </template>
        </v-data-table>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  import moment from 'moment';
  export default {
    name: 'RecentTableComponent',
    data () {
      return {
        dialog: false,
        selected: [],
        headers: [
          { text: '타입', value: 'type', width: '10px', align: 'center' },
          { text: '이름',  sortable: 'false', value: 'name', width: '140px', align: 'left' },
          { text: '마지막으로 액세스한 날짜', value: 'updated_at', width: '100px', align: 'center' },
          { text: '소유자', value: 'owner', width: '100px', align: 'center' },
          { text: '파일 크기', value: 'filesize', width: '100px', align: 'center' }
        ],
      }
    },
    computed: {
      files(){
        return this.$store.state.file.files
      }
    }
  }
</script>
