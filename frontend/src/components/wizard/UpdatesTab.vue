<template>
  <div>
    <updates-configuration :ethereum2config="this.model" />
  </div>
</template>

<script>
import UpdatesConfiguration from '../commons/UpdatesConfiguration.vue';
export default {
  name: "Ethereum1NodesTab",
  components: {
    UpdatesConfiguration,
  },
  data() {
    return {
    }
  },
  props: {
    model: Object,
  },
};
</script>

<style scoped></style>
