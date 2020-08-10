<template>
  <div>
    <file-navbar-component/>
    <data-table-component/>
  </div>
</template>

<script>
  import DataTableComponent from "../../components/DataTableComponent";
  import FileNavbarComponent from "../../components/FileNavbarComponent";
  export default {
    watchQuery: true,
    name: 'file',
    components: {
      FileNavbarComponent,
      DataTableComponent
    },
    async fetch({store, query}) {
      console.log('fetch 중', query.cid, query.owner);
      await store.dispatch('file/loadFiles', {cid: query.cid, owner: query.owner})
    }
  }
</script>
