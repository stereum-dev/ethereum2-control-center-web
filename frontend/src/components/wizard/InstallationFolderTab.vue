<template>
  <div class="text-left">
    <h3>Installation Path</h3>
    <div>
      <b-form-input
        v-model="model.installationFolder"
        placeholder="Enter installation path"
        :state="validation"
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

  computed: {
    validation() {
      return this.model.installationFolder.length > 0 && this.model.installationFolder.startsWith("/");
    },
  },
};
</script>

<style scoped></style>
