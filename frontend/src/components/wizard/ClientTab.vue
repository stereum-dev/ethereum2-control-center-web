<template>
  <div>
    <span> Please choose the client you want to use </span>
    <div class="text-left">
      <b-form-radio-group
        :stacked="true"
        label="Available Client Setups"
        :options="clients"
        v-model="model.client"
        value-field="id"
      >
      </b-form-radio-group>
    </div>
  </div>
</template>

<script>
export default {
  name: "WelcomeTab",
  components: {},
  data() {
    return {
      true: true,
      clients: [
        {
          id: "lighthouse",
          text: "Lighthouse by Sigma Prime",
          disabled: false,
        },
        { id: "lodestar", text: "Lodestar by Chainsafe", disabled: false },
        {
          id: "multiclient",
          text: "Multiclient using Lighthouse, Prysm, Teku with Vouch, Dirk",
          disabled: false,
        },
        { id: "nimbus", text: "Nimbus Eth2 by Status", disabled: false },
        { id: "prysm", text: "Prysm by Prysmatic Labs", disabled: false },
        { id: "teku", text: "Teku by ConsenSys", disabled: false },
      ],
    };
  },
  props: {
    model: Object,
  },
};
</script>

<style scoped></style>
