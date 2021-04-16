<template>
  <div>
    <span>
      Please enter the path to use to install Stereum's Etherium 2.0 node
    </span>
    <div>
      <b-form-input v-model="model.installationFolder" placeholder="Enter installation path"></b-form-input>      
    </div>
  </div>
</template>

<script>

export default {
  name: "InstallationFolderTab",
  components: { },
  props: {    
    model: Object,
  },
};
</script>

<style scoped>
</style>
