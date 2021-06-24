<template>
  <div class="text-left">
    <h3>Ethereum 1 Node URLs</h3>
    <div class="text-left">
      <div>
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
              :disabled="0 == items.indexOf(row.item)"
            >
              <b-icon icon="caret-up" aria-hidden="true"></b-icon>
            </b-button>
            <b-button
              size="sm"
              @click="moveItemDown(row)"
              variant="success"
              class="mb-2 mr-sm-2 mb-sm-0"
              :disabled="items.length - 1 == items.indexOf(row.item)"
            >
              <b-icon icon="caret-down" aria-hidden="true"></b-icon>
            </b-button>
          </template>
        </b-table>
      </div>
      <div>
        <b-form inline>
          <label class="mb-2 mr-sm-2 mb-sm-0" for="inline-new-url"
            >Ethereum 1 node URL (e. g. infura.io):</label
          >
          <b-form-input
            id="input-new-url"
            v-model="newUrl"
            placeholder="Enter new URL for Ethereum 1 node (e. g. infura.io)"
            class="mb-2 mr-sm-2 mb-sm-0 w-50"
            :state="validation"
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
  </div>
</template>

<script>
export default {
  name: "Ethereum1NodesTab",
  components: {},
  data() {
    let defaultItems = [{ url: "http://geth:8545" }];
    this.model.eth1nodes = defaultItems.map(item => item.url);

    let eth1network = "mainnet";
    if (this.model.network !== "mainnet") {
      eth1network = "goerli";
    }

    return {
      items: defaultItems,
      fields: ["url", "actions"],
      newUrl:
        "https://" +
        eth1network +
        ".infura.io:443/v3/put-your-infura-id-here",
    };
  },
  watch: {
    "model.network": function () {
      let eth1network = "mainnet";
      if (this.model.network !== "mainnet") {
        eth1network = "goerli";
      }
      this.newUrl =
        "https://" +
        eth1network +
        ".infura.io:443/v3/put-your-infura-id-here";
    },
  },
  computed: {
    validation() {
      let regex = new RegExp("https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}[\\.[a-zA-Z0-9()]{1,6}]{0,1}\\b([-a-zA-Z0-9()@:%_\\\\+.~#?&\\/\\/=]*)");
      return regex.test(this.newUrl);
    },
  },
  methods: {
    removeItem(e) {
      console.log("removeItem: " + JSON.stringify(e));
      console.log("index: " + e.index);

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
      this.model.eth1nodes = this.items.map(item => item.url);
    },
  },
  props: {
    model: Object,
  },
};
</script>

<style scoped></style>
