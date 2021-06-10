<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Ethereum 1 Nodes</h2>
    </div>

    <div class="row">
      <div class="col-12">
        <b-table striped hover :items="items" :fields="fields">
          <template #cell(actions)="row">
            <b-button
              size="sm"
              @click="removeItem(row)"
              variant="danger"
              class="mb-2 mr-sm-2 mb-sm-0"
            >
              <b-icon icon="trash" aria-hidden="true"></b-icon>
            </b-button>
            <b-button
              size="sm"
              @click="moveItemUp(row)"
              variant="success"
              class="mb-2 mr-sm-2 mb-sm-0"
            >
              <b-icon icon="caret-up" aria-hidden="true"></b-icon>
            </b-button>
            <b-button
              size="sm"
              @click="moveItemDown(row)"
              variant="success"
              class="mb-2 mr-sm-2 mb-sm-0"
            >
              <b-icon icon="caret-down" aria-hidden="true"></b-icon>
            </b-button>
          </template>
        </b-table>
      </div>
      <div class="col-12">
        <b-form inline>
          <label class="mb-2 mr-sm-2 mb-sm-0" for="inline-new-url"
            >Ethereum 1 node URL (e. g. infura.io):</label
          >
          <b-form-input
            id="input-new-url"
            v-model="newUrl"
            placeholder="Enter new URL for Ethereum 1 node (e. g. infura.io)"
            class="mb-2 mr-sm-2 mb-sm-0 w-50"
          ></b-form-input>
          <b-button
            size="sm"
            @click="addItem"
            variant="primary"
            class="mb-2 mr-sm-2 mb-sm-0"
          >
            <b-icon icon="plus" aria-hidden="true"></b-icon>
          </b-button>
        </b-form>
      </div>
    </div>

    <div class="row">
      <div class="col-12 text-right">
          <b-button variant="primary" @click="saveConfig"> Save &amp; Apply </b-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Ethereum1Nodes",
  components: {},
  data() {
    let eth1network = "mainnet";
    if (this.ethereum2config.network !== "mainnet") {
      eth1network = "goerli";
    }

    return {
      items: this.ethereum2config.eth1nodes.map(eth1node => { 
        return {url: eth1node};
      }),
      fields: ["url", "actions"],
      newUrl:
        "https://" +
        eth1network +
        ".infura.io:443/v3/put-your-infura-id-here",
    };
  },
  methods: {
    removeItem(e) {
      this.items.splice(e.index, 1);

      this.saveToModel();
    },
    moveItemUp(e) {
      if (e.index > 0) {
        const new_index = e.index - 1;
        const old_index = e.index;

        if (new_index >= this.items.length) {
          var k = new_index - this.items.length + 1;
          while (k--) {
            this.items.push(undefined);
          }
        }
        this.items.splice(new_index, 0, this.items.splice(old_index, 1)[0]);
      }

      this.saveToModel();
    },
    moveItemDown(e) {
      if (e.index + 1 < this.items.length) {
        const new_index = e.index + 1;
        const old_index = e.index;

        if (new_index >= this.items.length) {
          var k = new_index - this.items.length + 1;
          while (k--) {
            this.items.push(undefined);
          }
        }
        this.items.splice(new_index, 0, this.items.splice(old_index, 1)[0]);
      }

      this.saveToModel();
    },
    addItem() {
      this.items.push({ url: this.newUrl });

      this.saveToModel();
    },

    saveToModel() {
      this.ethereum2config.eth1nodes = this.items.map(eth1url => eth1url.url);
    },

    saveConfig() {
      this.processChange("set-eth1-nodes", {
        eth1_nodes_updated: this.ethereum2config.eth1nodes,
      });
    },
  },
  props: {
    ethereum2config: Object,
    processChange: Function,
  },
};
</script>

<style scoped></style>
