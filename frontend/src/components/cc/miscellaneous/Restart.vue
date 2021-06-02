<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Restart</h2>
    </div>
    <div class="col-12 text-left">
      <span>Your device will be restarted in couple of minutes!</span>
    </div>
    <div class="row">
      <div class="col-12 text-right">
        <b-button @click="Restart()" variant="primary">Restart</b-button>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "Restart",
  components: {},
  data() {
    return {};
  },
  props: {
    model: Object,
  },
  methods: {
    Restart() {
      // todo
    },
  },
};
</script>

<style scoped></style>
