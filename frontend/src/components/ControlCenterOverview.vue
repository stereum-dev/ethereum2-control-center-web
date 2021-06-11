<template>
  <div>
    <b-navbar toggleable="lg" style="background-color: #336666">
      <b-navbar-brand @click="showHome()">
        <b-img
          src="/public/stereum_logo.png"
          width="30"
          height="30"
          class="d-inline-block align-top"
        />
        Stereum
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item @click="showServices()">Services</b-nav-item>
          <b-nav-item @click="showUpdates()">Updates</b-nav-item>
          <b-nav-item-dropdown no-caret>
            <template #button-content>
              <span class="text-white">Validator Keys</span>
            </template>
            <b-dropdown-item @click="showImportValidator()"
              >Import Accounts</b-dropdown-item
            >
            <b-dropdown-item @click="showListExitValidator()"
              >List Accounts</b-dropdown-item
            >
          </b-nav-item-dropdown>
          <b-nav-item @click="showMiscellaneous()">Miscellaneous</b-nav-item>

          <b-nav-item
            v-if="this.ethereum2config.setup === 'prysm'"
            href="http://localhost:8083"
            target=”_blank”
          >
            Prysm-UI
          </b-nav-item>
          <b-nav-item
            v-if="this.ethereum2config.override !== 'beacon-validator' && this.ethereum2config.setup !== 'allbeacons'"
            href="http://localhost:8082"
            target=”_blank”
          >
            Grafana
          </b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item
            v-if="this.ethereum2config.updates.available.length < 1"
            href="#"
            disabled
            >No updates available</b-nav-item
          >
          <b-nav-item
            v-if="this.ethereum2config.updates.available.length > 0"
            @click="showUpdates()"
            >Update
            {{ this.ethereum2config.updates.available }} available!</b-nav-item
          >
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <div v-if="this.content === 'home'">
      <home />
    </div>
    <div v-if="this.content === 'services'">
      <services-overview
        :ethereum2config="this.ethereum2config"
        :processStatus="processStatus"
        :readData="readData"
      />
    </div>
    <div v-if="this.content === 'updates'">
      <updates-overview
        :ethereum2config="this.ethereum2config"
        :processChange="processChange"
      />
    </div>
    <div v-if="this.content === 'importValidator'">
      <import-validator :processChange="processChange" />
    </div>
    <div v-if="this.content === 'listExitValidator'">
      <list-exit-validator :ethereum2config="this.ethereum2config" />
    </div>
    <div v-if="this.content === 'miscellaneous'">
      <miscellaneous-overview
        :ethereum2config="this.ethereum2config"
        :showGraffiti="showGraffiti"
        :showApiBindAddress="showApiBindAddress"
        :showEth1Nodes="showEth1Nodes"
        :processChange="processChange"
      />
    </div>
    <div v-if="this.content === 'graffiti'">
      <graffiti
        :ethereum2config="this.ethereum2config"
        :processChange="processChange"
      />
    </div>
    <div v-if="this.content === 'apiBindAddress'">
      <api-bind-address
        :ethereum2config="this.ethereum2config"
        :processChange="processChange"
      />
    </div>
    <div v-if="this.content === 'eth1nodes'">
      <ethereum-1-nodes
        :ethereum2config="this.ethereum2config"
        :processChange="processChange"
      />
    </div>

    <vue-fab mainBtnColor="#336666" icon="help_outline">
      <!-- Icons from here: https://fonts.google.com/icons -->
      <fab-item
        @clickItem="clickHelpItem"
        :idx="0"
        title="Email"
        icon="email"
        titleBgColor="#336666"
        titleColor="#FFFFFF"
        color="#336666"
      />
      <fab-item
        @clickItem="clickHelpItem"
        :idx="1"
        title="Website"
        icon="language"
        titleBgColor="#336666"
        titleColor="#FFFFFF"
        color="#336666"
      />
      <fab-item
        @clickItem="clickHelpItem"
        :idx="2"
        title="Discord"
        icon="question_answer"
        titleBgColor="#336666"
        titleColor="#FFFFFF"
        color="#336666"
      />
    </vue-fab>

    <b-modal
      ref="control-changes-window"
      title="Applying"
      size="l"
      hide-footer
    >
      <div v-if="this.processStatus.running">
        <div class="alert alert-primary" role="alert">
          <b>Changes in Progress, please be patient</b>&nbsp;<i
            class="fas fa-cog fa-spin"
          ></i>
          <div>
            <b-progress          
            :value="this.processStatus.progress"
            variant="info"
            :max="100"
            show-progress
            animated
            >
              <b-progress-bar :value="this.processStatus.progress">
                <span
                  >Progress: <strong>{{ this.processStatus.progress.toFixed(0) }}%</strong></span
                >
              </b-progress-bar>
            </b-progress>
          </div>
        </div>
      </div>
      
      <div v-if="this.processStatus.success === true">
        <div class="alert alert-success" role="alert">
          Changes Successful!
        </div>
      </div>
      <div v-if="this.processStatus.success === false">
        <div class="alert alert-danger" role="alert">
          Unfortunately the changes failed, please consult logs for details!
        </div>
      </div>

      <ul class="list-group list-unstyled">
        <task-status-entry
          class="list-group-item text-left"
          v-bind:key="index"
          v-for="(status, index) in this.processStatus.logs.tasks"
          :model="status"
        ></task-status-entry>
      </ul>
    </b-modal>

    <b-overlay :show="processStatus.running" rounded="sm" no-wrap />
  </div>
</template>

<script>
//local registration
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import "@fortawesome/fontawesome-free/css/all.css";
import TaskStatusEntry from "@/components/commons/TaskStatusEntry.vue";
import Home from "@/components/cc/home/Home.vue";
import UpdatesOverview from "./cc/updates/UpdatesOverview.vue";
import ServicesOverview from "./cc/ServicesOverview.vue";
import ImportValidator from "./cc/validator/ImportValidator.vue";
import ListExitValidator from "./cc/validator/ListExitValidator.vue";
import MiscellaneousOverview from "./cc/miscellaneous/MiscellaneousOverview.vue";
import Graffiti from "./cc/miscellaneous/Graffiti.vue";
import ApiBindAddress from "./cc/miscellaneous/ApiBindAddress.vue";
import Ethereum1Nodes from "./cc/miscellaneous/Ethereum1Nodes.vue";
import axios from "axios";
import YAML from 'yaml';

export default {
  name: "ControlCenterOverview",
  components: {
    TaskStatusEntry,
    Home,
    UpdatesOverview,
    ServicesOverview,
    ImportValidator,
    ListExitValidator,
    MiscellaneousOverview,
    Graffiti,
    ApiBindAddress,
    Ethereum1Nodes,
  },
  data() {
    return {
      content: "home",
      processStatus: {
        response: "",
        logs: {
          tasks: [],
        },
        running: false,
        done: false,
        progress: 0,
        success: undefined,
      },
    };
  },
  created() {
    this.refreshConfig(this.showHome);
  },
  props: {
    ethereum2config: Object,
  },
  methods: {
    showHome() {
      this.content = "home";
    },
    showServices() {
      this.content = "services";
    },
    showUpdates() {
      //this.content = "updates";
      this.refreshConfig(this.showUpdatesAfterLoad);
    },
    showUpdatesAfterLoad() {
      this.content = "updates";
    },
    showImportValidator() {
      this.content = "importValidator";
    },
    showListExitValidator() {
      this.content = "listExitValidator";
    },
    showMiscellaneous() {
      this.content = "miscellaneous";
    },
    showGraffiti() {
      this.content = "graffiti";
    },
    showApiBindAddress() {
      this.content = "apiBindAddress";
    },
    showEth1Nodes() {
      this.content = "eth1nodes";
    },

    clickHelpItem: function (item) {
      if (item.idx == 2) {
        window.open("https://discord.gg/8Znj8K6GjN", "_blank");
      } else if (item.idx == 1) {
        window.open("https://stereum.net", "_blank");
      } else if (item.idx == 0) {
        window.location.href = "mailto:stereum@stereum.net";
      }
    },

    refreshConfig: function(callback) {
      this.readData("read-config", {}, this.refreshConfigModel, callback);
    },

    refreshConfigModel: function() {
      // read config to yaml
      let yaml = YAML.parse(this.processStatus.logs.tasks[1].message.stdout);

      // update model with yaml data
      this.ethereum2config.updates.available = yaml.update.available || "";
      this.ethereum2config.updates.lane = yaml.update.lane;
      this.ethereum2config.updates.unattended = [];
      if (yaml.update.unattended.check) {
        this.ethereum2config.updates.unattended.push("check");
      }
      if (yaml.update.unattended.install) {
        this.ethereum2config.updates.unattended.push("install");
      }

      this.ethereum2config.e2dc_graffiti = yaml.e2dc_graffiti;

      this.ethereum2config.e2dc_api_bind_address = yaml.e2dc_api_bind_address;

      this.ethereum2config.setup = yaml.setup;
      this.ethereum2config.override = yaml.setup_override;

      this.ethereum2config.network = yaml.network;

      this.ethereum2config.eth1nodes = yaml.connectivity.eth1_nodes;
    },

    readData: function(control, data, ...callbacks) {
      if (this.processStatus.running === false) {
        this.processStatus.running = true;
        this.processStatus.progress = 0;
        this.processStatus.done = false;
        this.processStatus.success = undefined;
        this.processStatus.logs = { tasks: [], };

        const payload = {
          inventory: "inventory.yaml",
          playbook: control + ".yaml",
          extra_vars: data,
          extraVars: data,
        };

        const fetchStatus = () => {
          axios.get("/api/setup/status").then((response) => {
            //console.log(response.data);
            this.processStatus.logs = response.data;
            this.processStatus.progress = response.data.tasks.length;
            callbacks.forEach(cb => cb.apply());
          });
        };

        axios
          .post("/api/setup/start", payload)
          .then((response) => {
            //console.log("Response data: " + response.data);
            if (response.data.status > 0) {
              this.$toasted.error(
                "Unfortunately the read data seems to have failed",
                { duration: 5000 }
              );
              this.processStatus.progress = 0;
              this.processStatus.success = false;
            }
            if (response.data.status == 0) {
              this.$toasted.success("date read successful!", {
                duration: 5000,
              });
              this.processStatus.progress = 100;
              this.processStatus.success = true;
            }
            this.processStatus.running = false;
            this.processStatus.done = true;
            fetchStatus(); // do a final status fetch
          })
          .catch((error) => {
            if (error.message == 'data read: Request failed with status code 404') {
              this.$toasted.error(
                "data read: Backend not reachable (http return code 404).",
                { duration: 5000 }
              );
            } else {
              this.$toasted.error(
                "data read:Unfortunately an error has occured during the changes",
                { duration: 5000 }
              );
            }
            console.error(error);
            this.processStatus.progress = 0;
            this.processStatus.running = false;
            this.processStatus.done = true;
          });
      }
    },

    processChange: function (control, data) {
      if (this.processStatus.running === false) {
        this.processStatus.running = true;
        this.processStatus.progress = 0;
        this.processStatus.done = false;
        this.processStatus.success = undefined;
        this.processStatus.logs = { tasks: [], };

        const payload = {
          inventory: "inventory.yaml",
          playbook: control + ".yaml",
          extra_vars: data,
          extraVars: data,
        };

        const fetchStatus = () => {
          axios.get("/api/setup/status").then((response) => {
            //console.log(response.data);
            this.processStatus.logs = response.data;
            this.processStatus.progress = response.data.tasks.length;
          });
        };
        let logWatchHandle = setInterval(fetchStatus, 1500);

        this.$refs["control-changes-window"].show();

        axios
          .post("/api/setup/start", payload)
          .then((response) => {
            //console.log("Response data: " + response.data);
            if (response.data.status > 0) {
              this.$toasted.error(
                "Unfortunately the changes seems to have failed",
                { duration: 5000 }
              );
              this.processStatus.progress = 0;
              this.processStatus.success = false;
            }
            if (response.data.status == 0) {
              this.$toasted.success("Changes done successfully!", {
                duration: 5000,
              });
              this.processStatus.progress = 100;
              this.processStatus.success = true;
            }
            this.processStatus.running = false;
            this.processStatus.done = true;
            fetchStatus(); // do a final status fetch
            clearInterval(logWatchHandle);
          })
          .catch((error) => {
            if (error.message == 'Request failed with status code 404') {
              this.$toasted.error(
                "Backend not reachable (http return code 404).",
                { duration: 5000 }
              );
            } else {
              this.$toasted.error(
                "Unfortunately an error has occured during the changes",
                { duration: 5000 }
              );
            }
            console.error(error);
            this.processStatus.progress = 0;
            this.processStatus.running = false;
            this.processStatus.done = true;
            clearInterval(logWatchHandle);
          });
      } else {
        this.$toasted.error("Changes in progress, please try later!", {
          duration: 5000,
        });
      }
    },
  },
};
</script>

<style scoped>
.nav-link {
  color: white !important;
}
.text-white {
  color: rgba(255, 255, 255, 1);
}
.navbar-brand {
  color: white !important;
}
.fab-main-container {
  right: 5% !important;
}
</style>
