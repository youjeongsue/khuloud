<template>
  <div>
    <star-table-component/>
  </div>
</template>

<script>
  import StarTableComponent from "../../components/StarTableComponent";

  export default {
    name: 'starred',
    components: {
      StarTableComponent
    },
    async fetch() {
      console.log('trash created 중');
      await this.$store.dispatch('file/loadStarFiles');
    }
  }
</script>
