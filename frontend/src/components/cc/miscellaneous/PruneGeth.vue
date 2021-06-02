<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Prune Geth</h2>
    </div>
    <div class="col-12 text-left">
      <span>It will delete several of your Ethereum 1 client - Geth's data to free up some storage space</span>
    </div>
    <div class="row">
      <div class="col-12 text-right">
        <b-button @click="gethPrune()" variant="primary">Prune Geth</b-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PruneGeth",
  components: {},
  data() {
    return {};
  },
  props: {
    model: Object,
  },
  methods: {
    gethPrune() {
      // todo
    },
  },
};
</script>

<style scoped></style>
