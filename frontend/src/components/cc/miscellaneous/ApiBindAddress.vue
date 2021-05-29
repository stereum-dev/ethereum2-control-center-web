<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>API Bind Address</h2>
    </div>

    <div class="row">
      <div class="col-12 text-right">
        <b-form>
          <b-form-group>
            <b-form-input v-model="apiBindAddress"></b-form-input>
          </b-form-group>
          <b-button variant="primary"> Save &amp; Apply </b-button>
        </b-form>
      </div>
    </div>
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
  },
  mounted() {
    this.apiBindAddress = this.ethereum2config.e2dc_api_bind_address;
  },
};
</script>

<style scoped></style>
