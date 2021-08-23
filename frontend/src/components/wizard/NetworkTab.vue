<template>
  <div class="text-left">
    <h3>Network</h3>
    <b-alert show variant="info">
      Here you can choose on which network your beacon node should run. The mainnet is the main Ethereum network that uses ETH for staking. For testing purposes choose the recommended Prater testnet, using its own brand of G&ouml;ETH. If you plan on staking with your ETH, be careful: Do not send real ETH to the testnet deposit contract! They will be lost!
    </b-alert>
    <div class="text-center">
      <b-form-radio-group
        :stacked="true"
        label="Available ETH2 Networks"
        :options="networks"
        v-model="model.network"
        value-field="id"
        buttons
        button-variant="outline-dark"
      >
      </b-form-radio-group>
    </div>
  </div>
</template>

<script>
export default {
  name: "NetworkTab",
  components: {},
  data() {
    return {
      true: true,
      networks: [
        { id: "mainnet", text: "Mainnet", disabled: false },
        { id: "prater", text: "Prater - long term testnet", disabled: false },
      ],
    };
  },
  props: {
    model: Object,
  },
};
</script>

<style scoped></style>
