<template>
  <sign-up-component/>
</template>

<script>
  import SignUpComponent from "../components/SignUpComponent";
  import LoginLayout from "../layouts/FormLayout";
  export default {
    name: 'register',
    layout: 'FormLayout',
    components: {SignUpComponent},
    data() {
      return {

      }
    }
  }
</script>
