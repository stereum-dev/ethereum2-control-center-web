<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Graffiti</h2>
    </div>

    <b-form>
      <div class="row">
        <div class="col-12">
            <b-form-group>
              <b-form-input v-model="graffiti" :state="validation"></b-form-input>
            </b-form-group>
        </div>
      </div>
      <div class="row">
        <div class="col-6 text-left">
          <b-button variant="warning" @click="resetToDefault"> Reset to Default </b-button>
        </div>
        <div class="col-6 text-right">
          <b-button variant="primary" @click="saveGraffiti"> Save Graffiti </b-button>
        </div>
      </div>
    </b-form>
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
    processChange: Function,
  },
  mounted() {
    this.graffiti = this.ethereum2config.e2dc_graffiti;
  },
  computed: {
    validation() {
      return this.graffiti.length < 33;
    },
  },
  methods: {
    saveGraffiti() {
      this.processChange("set-graffiti", 6, {
        e2dc_graffiti_updated: this.graffiti,
      });
    },

    resetToDefault() {
      this.graffiti = "stereum.net";
    },
  },
};
</script>

<style scoped></style>
