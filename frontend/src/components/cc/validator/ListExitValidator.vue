<template>
  <div class="container">
    <div class="row pb-3 pt-3 text-left">
      <div class="col-6">
        <h2>Validators</h2>
      </div>
      <div class="col-6 text-right">
        <b-button variant="success" @click="refreshAccounts">
          <b-icon icon="arrow-clockwise" aria-hidden="true"></b-icon>
          Refresh
        </b-button>
      </div>
    </div>
    <div class="row">
      <b-table striped hover :items="accounts" :fields="fields">
        <template #cell(ste)="row">
          <b-icon-question
            font-scale="2"
            v-if="
              row.item.length == 0
            "
          />
          <b-img src="/public/ste_favicon.png" width="32" height="32" v-else />
        </template>

        <template #cell(pubkey)="row">
          <div>
            {{ row.item }}
          </div>
        </template>

        <template #cell(balance)="row">
          <p>{{ row.item.Balance }}</p>
        </template>

        <template #cell(state)="row">
          <b-icon-check-square
            variant="success"
            font-scale="2"
            v-b-icon-check-square.hover
            title="Active"
            v-if="row.item.State === 'Active'"
          />
          <b-icon-dash-square
            variant="danger"
            font-scale="2"
            v-b-icon-dash-square.hover
            title="Inactive"
            v-else-if="row.item.State === 'Inactive'"
          />
          <b-icon-box-arrow-right
            variant="secondary"
            font-scale="2"
            v-icon-box-arrow-right.hover
            title="Exited"
            v-else-if="row.item.State === 'Exited'"
          />
          <b-icon-question-square
            variant="warning"
            font-scale="2"
            v-icon-question-square.hover
            title="Unknown state"
            v-else
          />
        </template>

        <template #cell(actions)="row">
          <b-button
            size="sm"
            @click="exitValidator(row)"
            variant="info"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-door-open.hover
            title="exit validator"
          >
            <b-icon icon="door-open" aria-hidden="true"></b-icon>
          </b-button>

          <b-button
            size="sm"
            @click="openBeaconcha()"
            variant="primary"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-link.hover
            title="go to https://beaconcha.in"
          >
            <b-icon icon="link" aria-hidden="true"></b-icon>
          </b-button>

          <b-button
            size="sm"
            @click="removeValidator(row)"
            variant="secondary"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-door-open.hover
            title="remove validator"
          >
            <b-icon icon="dash-circle" aria-hidden="true"></b-icon>
          </b-button>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "ListValidator",
  components: {},
  data() {
    return {
      accounts: [],
      fields: [
        { key: "ste", sortable: false, label: "" },
        { key: "pubkey", sortable: false, label: "Validator public key" },
        { key: "balance", sortable: false, label: "Balance" },
        { key: "state", sortable: false, label: "State" },
        { key: "actions", sortable: false },
      ],
    };
  },
  props: {
    ethereum2config: Object,
    processStatus: Object,
    readData: Function,
  },
  methods: {
    openBeaconcha: function () {
      window.open("https://beaconcha.in/", "_blank");
    },

    refreshAccounts: function() {
      this.readData("list-validator-accounts", {}, this.refreshAccountsModel);
    },

    refreshAccountsModel() {
      const regex = /0x[a-fA-F0-9]{96}/g;
      if (this.ethereum2config.setup == 'lighthouse' || this.ethereum2config.setup == 'nimbus') {
        this.accounts = this.processStatus.logs.tasks[2].message.stdout.match(regex)
      } 
      else if (this.ethereum2config.setup == 'lodestar' || this.ethereum2config.setup == 'prysm') { 
        this.accounts = this.processStatus.logs.tasks[3].message.stdout.match(regex);
      }  
    },

    exitValidator() {},

    removeValidator() {},
  },
  beforeMount(){
    this.refreshAccounts()
  },
};
</script>

<style scoped></style>
