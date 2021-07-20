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
      <b-table striped hover :items="accounts" :fields="fields" foot-clone>
        <template #cell(ste)="row">
          <b-icon-question
            font-scale="2"
            v-if="
              row.item.pubkey.length == 0
            "
          />
          <b-img src="/public/ste_favicon.png" width="32" height="32" v-else />
        </template>

        <template #cell(pubkey)="row">
          <div>
            {{ row.item.pubkey.substring(0,10) }}...{{ row.item.pubkey.substring(row.item.pubkey.length - 4, row.item.pubkey.length) }}
          </div>
        </template>

        <template #foot(pubkey)="data">
          <div class="text-right">
            &nbsp;
          </div>
        </template>

        <template #cell(balance)="row">
          <div>
            <div v-if="row.item.balance" class="text-right">
              &Xi; {{ row.item.balance / 1000000000 }}
            </div>
            <div v-else class="text-right">
              (unknown)
            </div>
          </div>
        </template>

        <template #foot(balance)="data">
          <div class="text-right">
            &Xi; {{ balanceTotal / 1000000000 }}
          </div>
        </template>

        <template #cell(state)="row">
          <div>
            <div v-if="row.item.status">
              <b-icon 
                v-if="row.item.status == 'active_online'"
                icon="minecart-loaded"
                variant="success"
                font-scale="2"
                v-b-tooltip.hover
                title="Staking - online" />
              <b-icon
                v-if="row.item.status == 'active_offline'"
                icon="minecart"
                variant="warning"
                font-scale="2"
                v-b-tooltip.hover
                title="Staking - but offline" />
              <b-icon
                v-if="row.item.status == 'slashed'"
                icon="exclamation-triangle"
                variant="danger"
                font-scale="2"
                v-b-tooltip.hover
                title="Slashed" />
              <b-icon
                v-if="row.item.status == 'pending'"
                icon="clock"
                variant="success"
                font-scale="2"
                v-b-tooltip.hover
                title="Pending - waiting for activation" />
            </div>
            <div v-else>
              <b-icon icon="question" 
                variant="info"
                font-scale="2"
                v-b-tooltip.hover
                title="No deposit observed yet" />
            </div>
          </div>
        </template>

        <template #foot(state)="data">
          <div class="text-right">
            &nbsp;
          </div>
        </template>


        <template #cell(actions)="row">
<!--
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
            @click="removeValidator(row)"
            variant="secondary"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-door-open.hover
            title="remove validator"
          >
            <b-icon icon="dash-circle" aria-hidden="true"></b-icon>
          </b-button>
-->
          <b-button
            size="sm"
            @click="copyPubKey(row)"
            variant="info"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="Copy public key to clipboard"
          >
            <b-icon icon="clipboard" aria-hidden="true"></b-icon>
          </b-button>
        </template>

        <template #foot(actions)="data">
          <div class="text-right">
            &nbsp;
          </div>
        </template>

      </b-table>
    </div>
    <div>
      Balance &amp; State data provided by beaconcha.in
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ListValidator",
  components: {},
  data() {
    return {
      accounts: [],
      balanceTotal: 0,
      fields: [
        { key: "ste", sortable: false, label: "" },
        { key: "pubkey", sortable: false, label: "Validator public key" },
        { key: "balance", sortable: false, label: "Balance" },
        { key: "state", sortable: false, label: "State" },
        { key: "actions", sortable: false, label: "Actions" },
      ],
    };
  },
  props: {
    ethereum2config: Object,
    processStatus: Object,
    readData: Function,
  },
  methods: {
    copyPubKey: function(row) {
      navigator.clipboard.writeText(row.item.pubkey).then(function() {
        this.$toasted.success("Copied public key to clipboard", {
          duration: 5000,
        });
      }, function(err) {
        this.$toasted.error(
          "Unfortunately there was an error copying the public key to clipboard!",
          { duration: 5000 }
        );
      });
    },

    refreshAccounts: function() {
      this.readData("list-validator-accounts", {}, this.refreshAccountsModel);
    },

    refreshAccountsModel() {
      let validatorKeys;
      const regex = /0x[a-fA-F0-9]{96}/g;
      const regex_teku = /[a-fA-F0-9]{96}/g;

      if (this.ethereum2config.setup == 'lighthouse' || this.ethereum2config.setup == 'nimbus') {        
        validatorKeys = this.processStatus.logs.tasks[2].message.stdout.match(regex)
      }

      else if (this.ethereum2config.setup == 'lodestar' || this.ethereum2config.setup == 'prysm') {
        validatorKeys = this.processStatus.logs.tasks[3].message.stdout.match(regex);
      }

      else if (this.ethereum2config.setup == 'teku' ) {            
        if (this.processStatus.logs.tasks.length == 9) {
          validatorKeys = this.processStatus.logs.tasks[7].message.stdout.match(regex_teku);
            for(let i=0; i<validatorKeys.length; i++) {
            validatorKeys[i]="0x"+validatorKeys[i];
          }    
        }

        else {
          validatorKeys = this.processStatus.logs.tasks[6].message.stdout.match(regex_teku)
        } 
      }

      if (validatorKeys != null) {
        let pubKeys = "";

        for(let i=0; i<validatorKeys.length; i++) {
          let validatorKey = validatorKeys[i];
          pubKeys = pubKeys + validatorKey + ",";
        }

        this.accounts = [];
        this.balanceTotal = 0;

        // cut last ','

        if (pubKeys.length > 0) {
          pubKeys = pubKeys.substring(0, pubKeys.length - 1);
          let network = "";
          if (this.ethereum2config.network != "mainnet") {
            network = this.ethereum2config.network + ".";
          }

          axios.get("https://" + network + "beaconcha.in/api/v1/validator/" + encodeURIComponent(pubKeys)).then((response) => {
            let data = response.data.data;
            for(let i=0; i<validatorKeys.length; i++) {
              let validatorKey = validatorKeys[i];
              let found = false;
              if (data.length > 1) {
                for (let i=0; i<data.length; i++) {
                  let dataKey = data[i];
                  if (validatorKey == dataKey.pubkey) {
                    this.accounts.push(dataKey);
                    this.balanceTotal = this.balanceTotal + dataKey.balance;
                    found = true;
                    break;
                  }
                }
              }

              else {
                if (validatorKey == data.pubkey) {
                  this.accounts.push(data);
                  this.balanceTotal = this.balanceTotal + dataKey.balance;
                  found = true;
                  break;
                  }
              }

              if (!found) {
                this.accounts.push({pubkey: validatorKey});
              }
            }
            console.log(this.accounts);
          });
        }  
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
