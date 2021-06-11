<template>
  <div class="text-left">
    <h3>Client(s) Customization</h3>
    <div class="text-left">
      <b-form-radio-group
        :stacked="true"
        label="Customize your setup"
        :options="overrides"
        v-model="model.override"
        value-field="id"
      >
      </b-form-radio-group>
    </div>
  </div>
</template>

<script>
export default {
  name: "CustomizeTab",
  components: {},
  data() {
    let overrides = [];

    this.addDefaultChoice(overrides);

    return {
      return: true,
      overrides: overrides,
    };
  },
  methods: {
    addDefaultChoice(choices) {
      this.addChoice(
        choices,
        "default",
        "No changes to the chosen setup apply"
      );
    },
    addChoice(choices, id, text) {
      choices.push({
        id: id,
        text: text,
        disabled: false,
      });
    },
  },
  watch: {
    "model.client": function (n) {
      this.overrides.splice(0, this.overrides.length);

      this.addDefaultChoice(this.overrides);

      if (n === "lighthouse") {
        this.addChoice(
          this.overrides,
          "no-geth",
          "Configuration without geth, using an external Ethereum 1 node (like infura.io)"
        );
      } else if (n === "lodestar") {
        this.addChoice(
          this.overrides,
          "no-geth",
          "Configuration without geth, using an external Ethereum 1 node (like infura.io)"
        );
      } else if (n === "multiclient") {
        this.addChoice(
          this.overrides,
          "limit-resources",
          "Default configuration with resource limits per container"
        );
      } else if (n === "nimbus") {
        this.addChoice(
          this.overrides,
          "no-geth",
          "Configuration without geth, using an external Ethereum 1 node (like infura.io)"
        );
      } else if (n === "prysm") {
        this.addChoice(
          this.overrides,
          "beacon-validator",
          "Beacon and validator only, no monitoring except Prysm Web UI"
        );
        this.addChoice(
          this.overrides,
          "geth-cache-2k",
          "Default configuration with geth cache 2000"
        );
        this.addChoice(
          this.overrides,
          "time-mount",
          "Default configuration with forced time sync of containers with host os (linux only)"
        );
      } else if (n === "teku") {
        this.addChoice(
          this.overrides,
          "no-geth",
          "Configuration without geth, using an external Ethereum 1 node (like infura.io)"
        );
      }
    },
  },
  props: {
    model: Object,
  },
};
</script>

<style scoped></style>
