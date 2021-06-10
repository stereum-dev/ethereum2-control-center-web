<template>
  <div>
    <div class="mt-3 mr-5 ml-5 mb-3" v-if="this.content === 'miscellaneousOverview'">
      <b-card-group columns>
        <b-card title="Graffiti" style="max-width: 20rem">
          <b-card-text>
            Set a mark on the beacon chain by choosing your own graffiti. This
            text will be included in every block your validator keys are propsing
            and visible for everybody!
          </b-card-text>

          <b-button @click="this.showGraffiti" variant="primary"
            >Set Graffiti</b-button
          >
        </b-card>
        <b-card
          title="API Bind Address"
          sub-title="Expert"
          style="max-width: 20rem"
        >
          <b-card-text>
            If you want to use your beacon client(s) or monitoring to be
            accessible outside of your server, configure on which IP the services
            should listen on.
          </b-card-text>

          <b-button @click="this.showApiBindAddress" variant="primary"
            >Set API Bind Address</b-button
          >
        </b-card>
        <b-card
          title="Ethereum 1 Connections"
          style="max-width: 20rem"
        >
          <b-card-text>
            Configure what Ethereum 1 nodes to use by specifying URLs to connect
            to for your beacon node, e. g. using your local geth as well as a
            Ethereum 1 service like infura.io for fallback.
          </b-card-text>

          <b-button @click="this.showEth1Nodes" variant="primary"
            >Set Ethereum 1 URLs</b-button
          >
        </b-card>
        <b-card title="Geth Prune" style="max-width: 20rem">
          <b-card-text>
            Geth is the Ethereum 1 client. It's collecting lots of data and some
            of it can be deleted again after some days. Run this to fee up some
            storage space again!
          </b-card-text>

          <b-button @click="showPruneGeth()" variant="primary">Prune Geth Now</b-button>
        </b-card>
        <b-card title="Restart Host" style="max-width: 20rem">
          <b-card-text>
            Sometimes there are things getting stuck or not responding anmore, a
            restart might help you resolve some issues (but not all). Keep in mind
            it might take a couple of minutes.
          </b-card-text>

          <b-button @click="showRestart()" variant="primary">Restart Now</b-button>
        </b-card>
        <b-card title="OS Update" style="max-width: 20rem;">
          <b-card-text>
            OS Updates will add new features to your device and improve existing ones.
            Also outdated features will be removed. Keep your device turned on during 
            the update process!
          </b-card-text>

          <b-button @click="showOSUpdate()" variant="primary">OS Update</b-button>
        </b-card>
      </b-card-group>
    </div>

    <div v-if="this.content === 'os-update'">
      <OSUpdate :processChange="processChange" />
    </div>

    <div v-if="this.content === 'prune-geth'">
      <PruneGeth :processChange="processChange" />
    </div>

    <div v-if="this.content === 'restart'">
      <Restart :processChange="processChange" />
    </div>
  </div>
</template>

<script>

import OSUpdate from "./OSUpdate.vue";
import PruneGeth from "./PruneGeth.vue";
import Restart from "./Restart.vue";

export default {
  name: "MiscellaneousOverview",
  data() {
    return {
      content: "miscellaneousOverview",
    };
  },
  components: {
    OSUpdate,
    PruneGeth,
    Restart,
  },
  props: {
    ethereum2config: Object,
    showGraffiti: Function,
    showApiBindAddress: Function,
    showEth1Nodes: Function,
    processChange: Function,
  },
  methods: {
    showOSUpdate() {
      this.content = "os-update";
    },
    showPruneGeth() {
      this.content = "prune-geth";
    },
    showRestart() {
      this.content = "restart";
    },
  },
};
</script>

<style scoped>
.card {
  margin: 0 auto; /* Added */
  float: none; /* Added */
  margin-bottom: 10px; /* Added */
}
</style>
