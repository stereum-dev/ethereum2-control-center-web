<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>SSV</h2>
    </div>

    <b-alert show variant="info">
      Register your operator with the public key below on https://docs.ssv.network/operators/installation-operator-1/registering-new-operator-on-the-ssv-network/register-via-interface
    </b-alert>

    <div class="row">
      <h4>Public Key (PK)</h4>
      <p style="word-break: break-all;">
        {{ ethereum2config.ssv.pk }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "SsvOverview",
  components: {},
  props: {
    ethereum2config: Object,
  },
};
</script>

<style scoped></style>
