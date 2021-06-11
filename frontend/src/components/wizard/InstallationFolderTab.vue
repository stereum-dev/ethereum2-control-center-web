<template>
  <div class="text-left">
    <h3>Installation Path</h3>
    <div>
      <b-form-input
        v-model="model.installationFolder"
        placeholder="Enter installation path"
      ></b-form-input>
    </div>
  </div>
</template>

<script>
export default {
  name: "InstallationFolderTab",
  components: {},
  props: {
    model: Object,
  },
};
</script>

<style scoped></style>
