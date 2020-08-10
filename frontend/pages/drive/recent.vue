<template>
  <div>
    <recent-table-component/>
  </div>
</template>

<script>
  import RecentTableComponent from "../../components/RecentTableComponent";
  export default {
    name: 'recent',
    components: {
      RecentTableComponent,
    },
    async fetch() {
      console.log('trash created 중');
      await this.$store.dispatch('file/loadRecentFiles');
    }
  }
</script>
