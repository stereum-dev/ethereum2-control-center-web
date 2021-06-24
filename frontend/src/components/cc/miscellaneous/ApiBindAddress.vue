<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>API Bind Address</h2>
    </div>

    <b-form>
      <div class="row">
        <div class="col-12">
          <b-form-group>
            <b-form-input v-model="apiBindAddress" :state="validation"></b-form-input>
          </b-form-group>
        </div>
      </div>
      <div class="row">
        <div class="col-6 text-left">
          <b-button variant="warning" @click="resetToDefault"> Reset to Default </b-button>
        </div>
        <div class="col-6 text-right">
          <b-button variant="primary" @click="saveApiBindAddress"> Save &amp; Apply </b-button>
        </div>
      </div>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "ApiBindAddress",
  components: {},
  data() {
    return {
      apiBindAddress: this.ethereum2config.e2dc_api_bind_address,
    };
  },
  props: {
    ethereum2config: Object,
    processChange: Function,
  },
  mounted() {
    this.apiBindAddress = this.ethereum2config.e2dc_api_bind_address;
  },
  computed: {
    validation() {
      let regex = new RegExp("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$");
      return regex.test(this.apiBindAddress);
    },
  },
  methods: {
    saveApiBindAddress() {
      this.processChange("set-api-bind-address", 6, {
        e2dc_api_bind_address_updated: this.apiBindAddress,
      });
    },
    resetToDefault() {
      this.apiBindAddress = "127.0.0.1";
    },
  }
};
</script>

<style scoped></style>
