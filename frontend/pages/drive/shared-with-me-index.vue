<template>
  <div>
    <share-navbar-component/>
    <share-list-component/>
  </div>
</template>

<script>
  import ShareNavbarComponent from "../../components/ShareNavbarComponent";
  import ShareListComponent from "../../components/ShareListComponent";

  export default {
    components: {ShareNavbarComponent, ShareListComponent},
    async fetch({store}) {
      console.log('fetch 중');
      await store.dispatch('file/loadShareFolder');
    }
  }
</script>
