<template>
  <div class="text-left">
    <h3>Network</h3>
    <div class="text-left">
      <b-form-radio-group
        :stacked="true"
        label="Available ETH2 Networks"
        :options="networks"
        v-model="model.network"
        value-field="id"
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
        { id: "prater", text: "Prater - testnet", disabled: false },
        { id: "pyrmont", text: "Pyrmont - testnet (will be offline soon)", disabled: false },
      ],
    };
  },
  props: {
    model: Object,
  },
};
</script>

<style scoped></style>
