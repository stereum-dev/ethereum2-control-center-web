<template>
  <div class="text-left">
    <h3>Client(s) Customization</h3>
    <b-alert show variant="info">
      In this step, you can choose between the following Customization Option for your installation.
    </b-alert>
    <div class="text-center">
      <b-form-radio-group
        :stacked="true"
        label="Customize your setup"
        :options="overrides"
        v-model="selectedOverride"
        value-field="id"
        buttons
        button-variant="outline-dark"
      >
      </b-form-radio-group>
    </div>

    <b-alert 
      v-if="ansibleFacts !== undefined && (selectedOverride.minCpus <= ansibleFacts.processor_vcpus || selectedOverride.minMemory <= ansibleFacts.memtotal_mb)"
      show
      variant="success"
      class="mt-3"
      >
      <b-container>
        <b-row>
          <b-col><b>Your server can handle the load of the configuration!</b></b-col>
        </b-row>
        <b-row>
          <b-col>CPU Cores (current/need):</b-col>
          <b-col class="text-right">{{ ansibleFacts.processor_vcpus }}/{{ selectedOverride.minCpus }}</b-col>
        </b-row>
        <b-row>
          <b-col>Memory (current/need):</b-col>
          <b-col class="text-right">{{ ansibleFacts.memtotal_mb }} mb/{{ selectedOverride.minMemory }} mb</b-col>
        </b-row>
      </b-container>
    </b-alert>
    <b-alert 
      v-else-if="ansibleFacts !== undefined"
      show
      variant="danger"
      class="mt-3"
      >
      <b>Your server might be too weak to run the selected configuration!</b><br/>
      CPU Cores (current/need): {{ ansibleFacts.processor_vcpus }}/{{ selectedOverride.minCpus }}<br/>
      Memory (current/need): {{ ansibleFacts.memtotal_mb }} mb/{{ selectedOverride.minMemory }} mb
    </b-alert>
  </div>
</template>

<script>
export default {
  name: "CustomizeTab",
  components: {},
  data() {
    let overrides = [];

    const defaultChoice = this.addDefaultChoice(overrides, 15000, 8);

    return {
      return: true,
      overrides: overrides,
      selectedOverride: defaultChoice.id,
    };
  },
  methods: {
    addDefaultChoice(choices, minMemory, minCpus) {
      return this.addChoice(
        choices,
        "default",
        "Default (install with Geth ETH1 Client)",
        minMemory,
        minCpus,
        true
      );
    },
    addChoice(choices, id, text, minMemory, minCpus, select = false) {
      const choice = {
        id: {
          id: id,
          minMemory: minMemory,
          minCpus: minCpus,
        },
        text: text,
        disabled: false,
      };

      choices.push(choice);

      if (select) {
        this.selectedOverride = choice.id;
      }

      return choice;
    },
  },
  watch: {
    "selectedOverride": function(n) {
      console.log(n);
      this.model.override = n.id;
      console.log("new model.override: " + this.model.override);
      this.$forceUpdate();
    },
    "model.client": function (n) {
      this.overrides.splice(0, this.overrides.length);

      if (n === "lighthouse") {
        this.addDefaultChoice(this.overrides, 7500, 4, true);
        this.addChoice(
          this.overrides,
          "no-geth",
          "Configuration without geth, using an external Ethereum 1 node (like infura.io)",
          3500,
          2
        );
        if (this.model.network == "prater") {
          this.addChoice(
            this.overrides,
            "ssv-no-geth",
            "SSV and no local geth",
            3500,
            2
          );
        }
      } else if (n === "allbeacons") {
        this.addDefaultChoice(this.overrides, 15000, 8, true);
      } else if (n === "lodestar") {
        this.addDefaultChoice(this.overrides, 7500, 4, true);
        this.addChoice(
          this.overrides,
          "no-geth",
          "Configuration without geth, using an external Ethereum 1 node (like infura.io)",
          3500,
          2
        );
      } else if (n === "multiclient") {
        this.addDefaultChoice(this.overrides, 15000, 8, true);
        this.addChoice(
          this.overrides,
          "limit-resources",
          "Default configuration with resource limits per container",
          15000,
          8
        );
      } else if (n === "nimbus") {
        this.addDefaultChoice(this.overrides, 7500, 4, true);
        this.addChoice(
          this.overrides,
          "no-geth",
          "Configuration without geth, using an external Ethereum 1 node (like infura.io)",
          3500,
          2
        );
      } else if (n === "prysm") {
        this.addDefaultChoice(this.overrides, 7500, 4, true);
        this.addChoice(
          this.overrides,
          "beacon-validator",
          "Beacon and validator only, no monitoring except Prysm Web UI",
          3500,
          2
        );
        this.addChoice(
          this.overrides,
          "geth-cache-2k",
          "Default configuration with geth cache 2000",
          7500,
          4
        );
        this.addChoice(
          this.overrides,
          "time-mount",
          "Default configuration with forced time sync of containers with host os (linux only)",
          7500,
          4
        );
      } else if (n === "teku") {
        this.addDefaultChoice(this.overrides, 7500, 4, true);
        this.addChoice(
          this.overrides,
          "no-geth",
          "Configuration without geth, using an external Ethereum 1 node (like infura.io)",
          3500,
          2
        );
      }
    },
  },
  props: {
    model: Object,
    ansibleFacts: Object,
  },
};
</script>

<style scoped></style>
