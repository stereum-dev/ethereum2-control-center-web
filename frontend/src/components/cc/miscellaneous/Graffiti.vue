<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Graffiti</h2>
    </div>

    <div class="row">
      <div class="col-12 text-right">
        <b-form>
          <b-form-group>
            <b-form-input v-model="graffiti"></b-form-input>
          </b-form-group>
          <b-button variant="primary"> Save Graffiti </b-button>
        </b-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Graffiti",
  components: {},
  data() {
    return {
      graffiti: this.ethereum2config.e2dc_graffiti,
    };
  },
  props: {
    ethereum2config: Object,
  },
  mounted() {
    this.graffiti = this.ethereum2config.e2dc_graffiti;
  },
};
</script>

<style scoped></style>
