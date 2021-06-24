<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Updates</h2>
    </div>
    <div class="row">
      <div class="col-6 pr-5">
        <updates-configuration :ethereum2config="this.ethereum2config" />

        <div class="container mt-3">
          <div class="row">
            <div>
              <p class="text-center">
                <b-button variant="primary" @click="saveUpdateConfig"> Save </b-button>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 pl-5">
        <manual-update :ethereum2config="this.ethereum2config" :checkForUpdates="checkForUpdates" :runUpdate="runUpdate" />
      </div>
    </div>
  </div>
</template>

<script>
import UpdatesConfiguration from "../../commons/UpdatesConfiguration.vue";
import ManualUpdate from "./ManualUpdate.vue";

export default {
  name: "UpdatesOverview",
  components: {
    UpdatesConfiguration,
    ManualUpdate,
  },
  data() {
    return {};
  },
  props: {
    ethereum2config: Object,
    processChange: Function,
    refreshConfig: Function,
    lockControlCenter: Function,
  },
  methods: {
    saveUpdateConfig() {
      let unattended_updates_check = this.ethereum2config.updates.unattended.indexOf(
        "check"
      ) > -1;
      let unattended_updates_install = this.ethereum2config.updates.unattended.indexOf(
        "install"
      ) > -1;

      this.processChange("configure-autoupdate", 6, {
          update: {
            lane: this.ethereum2config.updates.lane,
            unattended: {
              check: unattended_updates_check,
              install: unattended_updates_install,
            },
          },
        }, this.checkForUpdatedConfig);
    },

    checkForUpdatedConfig() {
      this.refreshConfig(function() {});
    },

    checkForUpdates() {
      this.processChange("update-check", 3, {}, this.checkForUpdatedConfig);
    },

    runUpdate() {
      this.processChange("unattended-update", 1, {}, this.lockControlCenter);
    },
  },
};
</script>

<style scoped></style>
