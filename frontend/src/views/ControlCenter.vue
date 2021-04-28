<template>
  <div class="control-center">
    <control-center-overview :ethereum2config="this.ethereum2config" />
  </div>
</template>

<script>
// @ is an alias to /src
import ControlCenterOverview from "@/components/ControlCenterOverview.vue";

export default {
  name: "ControlCenter",
  components: {
    ControlCenterOverview,
  },
  data() {
    return {
      ethereum2config: {
        network: "pyrmont",
        client: "lighthouse",
        installationFolder: "/opt/stereum",
        override: "default",
        eth1nodes: ["http://geth:8545", "https://goerli.infura.io/foo/bar"],
        updates: {lane: "rc", unattended: ["install"]},
      },
    };
  },
};
</script>
