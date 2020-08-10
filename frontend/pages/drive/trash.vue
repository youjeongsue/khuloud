<template>
  <div>
    <trash-table-component/>
  </div>
</template>

<script>
  import TrashTableComponent from "../../components/TrashTableComponent";

  export default {
    name: 'trash',
    components: {
      TrashTableComponent
    },
    async fetch() {
      console.log('trash created 중');
      await this.$store.dispatch('file/loadTrash');
    }
  }
</script>

<style>

</style>
