<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Update Operating System</h2>
    </div>
    <div class="col-12 text-left">
      <span>It is important to keep your device turned on during the update process! The server will restart if necessary, you might need to restart your launcher.</span>
    </div>
    <div class="row">
      <div class="col-12 text-right">
        <b-button @click="runOsUpdates()" variant="primary">Update OS</b-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "OSUpdate",
  components: {},
  data() {
    return {};
  },
  props: {
    ethereum2config: Object,
    processChange: Function,
  },
  methods: {
    runOsUpdates() {
      this.processChange("update-host-os", 5, {});
    },
  },
};
</script>

<style scoped></style>
