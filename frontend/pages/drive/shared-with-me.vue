<template>
  <div>
    <share-table-component/>
    <share-form-component/>
  </div>
</template>

<script>
  import ShareTableComponent from "../../components/ShareTableComponent";
  import ShareFormComponent from "../../components/ShareFormComponent";

  export default {
    watchQuery: true,
    name: 'shared-with-me',
    components: {
      ShareTableComponent,
      ShareFormComponent
    },
    async fetch({store, query}) {
      console.log('fetch 중', query.id);
      await store.dispatch('file/loadSingleShareFolder', {id: query.id});
      await store.dispatch('file/loadShareFile', {id: query.id});
      await store.dispatch('file/loadShareUser', {id: query.id});
    }
  }
</script>
