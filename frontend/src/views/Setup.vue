<template>
  <div class="setup">
    <setup-wizard :model="model" />
  </div>
</template>

<script>
// @ is an alias to /src
import SetupWizard from "@/components/SetupWizard.vue";

export default {
  name: "Setup",
  components: {
    SetupWizard,
  },
  data() {
    return {
      model: {
        network: "prater",
        client: "allbeacons",
        installationFolder: "/opt/stereum",
        override: "default",
        eth1nodes: [],
        updates: {},
        fastSync: false,
        exportedConfigFolder: "",
        importConfig: false,
        importValidator: false,
        configPassword: "",
        validatorPassword: "",
      },
    };
  },
};
</script>
