<template>
  <div class="control-center">
    <control-center-overview :model="model" />
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
      model: {
        network: "pyrmont",
        client: "allbeacons",
        installationFolder: "/opt/stereum",
        override: "default",
        eth1nodes: [],
        updates: {},
      },
    };
  },
};
</script>
