<template>
  <div class="text-left">
    <h3>Update manually</h3>

    <div class="mt-3">
      Update vailable:
      <strong v-if="ethereum2config.updates.available.length > 0"
        >Yes ({{ this.ethereum2config.updates.available }})</strong
      >
      <strong v-else>No</strong>
    </div>

    <div class="container mt-3">
      <div class="row">
        <div class="col-5">
          <p class="text-center">
            <b-button
              variant="primary"
              :disabled="this.ethereum2config.updates.available.length < 1"
            >
              Update now!
            </b-button>
          </p>
        </div>

        <div class="col-5">
          <p class="text-center">
            <b-button variant="primary"> Check for updates </b-button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ManualUpdate",
  components: {},
  data() {
    return {};
  },
  watch: {
    "update.lane": function () {
      this.newUrl =
        "https://" +
        this.ethereum2config.network +
        ".infura.io:443/v3/put-your-infura-id-here";
    },
  },
  methods: {},
  props: {
    ethereum2config: Object,
  },
};
</script>

<style scoped></style>
