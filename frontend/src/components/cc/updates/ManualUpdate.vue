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
              @click="confirmRunUpdate"
            >
              Update now!
            </b-button>
          </p>
        </div>

        <div class="col-5">
          <p class="text-center">
            <b-button variant="primary" @click="checkForUpdates"> Check for updates </b-button>
          </p>
        </div>
      </div>
    </div>
    <b-overlay :show="busy" no-wrap>
      <template #overlay>
        <div v-if="runningUpdate" class="text-center p-4 bg-primary text-light rounded">
          <b-icon icon="cloud-upload" font-scale="4"></b-icon>
          <div class="mb-3">Thank you for using Stereum Ethereum Node Setup! Updating now...</div>
        </div>
        <div
          v-else
          ref="dialog"
          tabindex="-1"
          role="dialog"
          aria-modal="false"
          aria-labelledby="form-confirm-label"
          class="text-center p-3"
        >
          <p><strong id="form-confirm-label">Web Control Center will be busy for a few minutes. Are you sure?</strong></p>
          <div class="d-flex ml-4 pl-3">
            <b-button variant="outline-danger" class="mr-4" @click="onCancel">
              Cancel
            </b-button>
            <b-button variant="outline-success" class="ml-4" @click="runUpdateConfirmed">OK</b-button>
          </div>
        </div>
      </template>
    </b-overlay>
  </div>
</template>

<script>
export default {
  name: "ManualUpdate",
  components: {},
  data() {
    return {
      runningUpdate: false,
      busy: false,
    };
  },
  watch: {
    "update.lane": function () {
      this.newUrl =
        "https://" +
        this.ethereum2config.network +
        ".infura.io:443/v3/put-your-infura-id-here";
    },
  },
  methods: {
    confirmRunUpdate() {
      this.busy = true;
    },
    onCancel() {
      this.busy = false;
    },
    runUpdateConfirmed() {
      this.runningUpdate = true;
      this.runUpdate();
    }
  },
  props: {
    ethereum2config: Object,
    checkForUpdates: Function,
    runUpdate: Function,
  },
};
</script>

<style scoped></style>
