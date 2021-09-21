<template>
  <div>
    <b-card
      img-src="/public/setup-banner.png"
      img-alt="Image"
      img-top
      tag="article"
      style="max-width: 20rem"
      class="mb-2 main-card"
    >
      <b-card-body>
        <div>
          <form-wizard
            shape="square"
            color="#336666"
            title="Stereum Ethereum Node Setup"
            subtitle=""
            finishButtonText="Start Installation"
            @on-complete="onComplete"
            :hide-buttons="installationRunning || installationSuccess"
          >
            <tab-content title="Welcome" icon="faw fas fa-compass">
              <welcome-tab :setAnsibleFacts="setAnsibleFacts"></welcome-tab>
            </tab-content>

            <tab-content 
              title="Import-Config" 
              icon="faw fas fa-file-import"
              :before-change="() => validateConfigFolder()"
            >
              <import-config-tab :model="model" :ansibleFacts="ansibleFacts"></import-config-tab>
            </tab-content>

            <tab-content v-if="this.model.importConfig == false" title="Network" icon="faw fas fa-network-wired">
              <network-tab :model="model" :disabled="model.importConfig === false"></network-tab>
            </tab-content>
            <tab-content v-if="this.model.importConfig == false" title="Client" icon="faw fas fa-cogs">
              <setup-tab :model="model"></setup-tab>
            </tab-content>
            <tab-content v-if="this.model.importConfig == false" title="Customize" icon="faw fas fa-wrench">
              <customize-tab :model="model" :ansibleFacts="ansibleFacts"></customize-tab>
            </tab-content>
            <tab-content v-if="this.model.importConfig == false" title="Ethereum 1 Nodes" icon="faw fas fa-database">
              <ethereum-1-nodes-tab :model="model"></ethereum-1-nodes-tab>
            </tab-content>
            <tab-content v-if="this.model.importConfig == false" title="Updates" icon="faw fas fa-sync">
              <updates-tab :model="model"></updates-tab>
            </tab-content>
            <tab-content
              v-if="this.model.importConfig == false" 
              title="Path"
              icon="faw far fa-folder-open"
              :before-change="() => validateInstallationFolder()"
            >
              <installation-folder-tab :model="model" :ansibleFacts="ansibleFacts"></installation-folder-tab>
            </tab-content>
            <tab-content title="Verify" icon="faw fas fa-check-double">
              <verification-tab
                :logs="logs.tasks"
                :model="model"
                :progress="installationProgress"
                :running="installationRunning"
                :success="installationSuccess"
                :done="installationDone"
                :ansibleFacts="ansibleFacts"
              ></verification-tab>
            </tab-content>
          </form-wizard>
        </div>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
//local registration
import { FormWizard, TabContent } from "vue-form-wizard";
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import "@fortawesome/fontawesome-free/css/all.css";
import WelcomeTab from "@/components/wizard/WelcomeTab.vue";
import ImportConfigTab from "@/components/wizard/ImportConfigTab.vue";
import NetworkTab from "@/components/wizard/NetworkTab.vue";
import SetupTab from "@/components/wizard/SetupTab.vue";
import CustomizeTab from "@/components/wizard/CustomizeTab.vue";
import Ethereum1NodesTab from "@/components/wizard/Ethereum1NodesTab.vue";
import UpdatesTab from "@/components/wizard/UpdatesTab.vue";
import InstallationFolderTab from "@/components/wizard/InstallationFolderTab.vue";
import VerificationTab from "@/components/wizard/VerificationTab.vue";
import axios from "axios";

export default {
  name: "SetupWizard",
  components: {
    FormWizard,
    TabContent,
    WelcomeTab,
    ImportConfigTab,
    NetworkTab,
    SetupTab,
    CustomizeTab,
    Ethereum1NodesTab,
    UpdatesTab,
    InstallationFolderTab,
    VerificationTab,
  },
  data() {
    return {
      response: "",
      logs: {
        tasks: [],
      },
      installationRunning: false,
      installationDone: false,
      installationProgress: 0,
      installationSuccess: undefined,
      ansibleFacts: undefined,
    };
  },
  props: {
    model: Object,
  },
  methods: {
    setAnsibleFacts: function(newAnsibleFacts) {
      this.ansibleFacts = newAnsibleFacts;
    },

    validateInstallationFolder() {
      return (
        this.model.installationFolder &&
        this.model.installationFolder.startsWith("/")
      );
    },

    validateConfigFolder() {
      if (this.model.importConfig == false) {
        return (
          this.model.exportedConfigFolder.length == 0 &&
          this.model.configPassword.length == 0 &&
          this.model.validatorPassword == "" 
        );  
      } else if (this.model.importConfig == true && this.model.importValidator == false) {
          return (
            this.model.exportedConfigFolder.length > 0 &&
            this.model.exportedConfigFolder.startsWith("/") &&
            this.model.exportedConfigFolder.endsWith(".zip") &&
            this.model.configPassword.length > 0 &&
            this.model.validatorPassword == ""
          );  
        } else if (this.model.importConfig == true && this.model.importValidator == true) {
            return (
              this.model.exportedConfigFolder.length > 0 &&
              this.model.exportedConfigFolder.startsWith("/") &&
              this.model.exportedConfigFolder.endsWith(".zip") &&
              this.model.configPassword.length > 0 &&
              this.model.validatorPassword.length > 0
            );  
          }
    },

    onComplete: function () {
      this.installationRunning = true;
      this.installationProgress = 0;

      let unattended_updates_check = this.model.updates.unattended.indexOf(
        "check"
      ) > -1;
      let unattended_updates_install = this.model.updates.unattended.indexOf(
        "install"
      ) > -1;

      // write variables for the ansible call
      
      let extraVars;
      if (this.model.importConfig == false && this.model.importValidator == false) {
        extraVars = {
          network: this.model.network,
          setup: this.model.client,
          setup_override: this.model.override || "default",
          connectivity: {
            eth1_nodes: this.model.eth1nodes,
          },
          update: {
            lane: this.model.updates.lane,
            unattended: {
              check: unattended_updates_check,
              install: unattended_updates_install,
            },
          },
          install_path: this.model.installationFolder,
          stereum_version_tag: window.STEREUM_VERSION_TAG,
          load_blockchain_db: this.model.fastSync,
        }; 
      } 
      else if (this.model.importConfig == true && this.model.importValidator == false) {
        extraVars = {
          exported_config_path: this.model.exportedConfigFolder,
          exported_config_password: this.model.configPassword,
        };
      }
      else if (this.model.importConfig == true && this.model.importValidator == true) {
        extraVars = {
          exported_config_path: this.model.exportedConfigFolder,
          exported_config_password: this.model.configPassword,
          validator_password: this.model.validatorPassword,
        };
      }

      const payload = {
        inventory: "inventory.yaml",
        playbook: "playbook.yaml",
        extra_vars: extraVars,
        extraVars: extraVars,
      };

      this.installationDone = false;

      const finishInstallation = () => {
        this.$toasted.success(
          "Installation done successfully, have fun using Stereum",
          { duration: 5000 }
        );
        this.installationProgress = 100;
        this.installationSuccess = true;

        this.installationRunning = false;
        this.installationDone = true;
      };

      let logWatchHandle;
      const fetchStatus = () => {
        axios.get("/api/setup/status").then((response) => {
          console.log(response.data);
          this.logs = response.data;

          let maxTasks = 65;
          if (this.model.fastSync) {
            maxTasks = maxTasks + 6;
          }

          this.installationProgress = response.data.tasks.length / maxTasks * 100;

          const lastTask = response.data.tasks[response.data.tasks.length - 1];
          if (lastTask.name == 'Start services' && lastTask.status == 0) {
            finishInstallation();
            clearInterval(logWatchHandle);
          }
        });
      };
      logWatchHandle = setInterval(fetchStatus, 30000);

      axios
        .post("/api/setup/start", payload)
        .then((response) => {
          console.log(response.data);
          if (response.data.status > 0) {
            this.$toasted.error(
              "Unfortunately the installtion seems to have failed",
              { duration: 5000 }
            );
            this.installationProgress = 0;
            this.installationSuccess = false;
          }
          if (this.installationRunning) {
            if (response.data.status == 0) {
              this.$toasted.success(
                "Installation done successfully, have fun using Stereum",
                { duration: 5000 }
              );
              this.installationProgress = 100;
              this.installationSuccess = true;
            }
            this.installationRunning = false;
            this.installationDone = true;
            fetchStatus(); // do a final status fetch
            clearInterval(logWatchHandle);
          }
        })
        .catch((error) => {
          this.$toasted.error(
            `Unfortunately an error has occured during the installation: ${error}`,
            { duration: 5000 }
          );
          console.error(error);
          this.installationProgress = 0;
          this.installationRunning = false;
          this.installationDone = true;
          clearInterval(logWatchHandle);
        });
    },
  },
};
</script>

<style scoped>
.main-card {
  margin-top: 10px;
  margin-left: 5%;
  margin-right: 5%;
  min-width: 90%;
}

.main-card img {
  max-height: 50px;
}

.card-body {
  padding: 0.5rem;
}

.vue-form-wizard {
  padding-bottom: 0px;
}

</style>
