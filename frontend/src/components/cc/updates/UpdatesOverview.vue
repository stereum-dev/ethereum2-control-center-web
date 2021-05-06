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
                <b-button variant="primary"> Save </b-button>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 pl-5">
        <manual-update :ethereum2config="this.ethereum2config" />
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
  },
};
</script>

<style scoped></style>
