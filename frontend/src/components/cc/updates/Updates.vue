<template>
  <div>
    <h1>Unattended automized updates configuration</h1>
    <updates-configuration :ethereum2config="this.ethereum2config" />
  </div>
</template>

<script>
import UpdatesConfiguration from '../../commons/UpdatesConfiguration.vue';
export default {
  name: "Updates",
  components: {
    UpdatesConfiguration,
  },
  data() {
    return {
    };
  },
  props: {
    ethereum2config: Object,
  },
};
</script>

<style scoped></style>
