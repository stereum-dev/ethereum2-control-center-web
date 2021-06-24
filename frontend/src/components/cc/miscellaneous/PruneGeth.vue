<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Prune Geth</h2>
    </div>
    <div class="col-12 text-left">
      <span>It will delete several unnecessary data of your Ethereum 1 client's database to free up some storage space! The process can take up to several hours, it'll run in the background and restart geth as soon as it's done.</span>
    </div>
    <div class="row">
      <div class="col-12 text-right">
        <b-button @click="gethPrune" variant="primary">Prune Geth</b-button>
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
    processChange: Function,
  },
  methods: {
    gethPrune() {
      this.processChange("geth-prune", 3, {});
    },
  },
};
</script>

<style scoped></style>
