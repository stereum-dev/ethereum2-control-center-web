<template>
  <div>
    <b-navbar toggleable="lg" style="background-color: #336666">
      <b-navbar-brand @click="showHome()">
        <b-img src="/public/stereum_logo.png" width="30" height="30" class="d-inline-block align-top" /> Stereum
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
              >Import Account</b-dropdown-item
            >
            <b-dropdown-item @click="showListValidator()"
              >List Account</b-dropdown-item
            >
            <b-dropdown-item @click="showExitValidator()"
              >Exit Account</b-dropdown-item
            >
          </b-nav-item-dropdown>
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
      <services-overview :ethereum2config="this.ethereum2config" />
    </div>
    <div v-if="this.content === 'updates'">
      <updates-overview :ethereum2config="this.ethereum2config" />
    </div>
    <div v-if="this.content === 'importValidator'">
      <import-validator />
    </div>
    <div v-if="this.content === 'listValidator'">
      <list-validator />
    </div>
    <div v-if="this.content === 'exitValidator'">
      <exit-validator />
    </div>
  </div>
</template>

<script>
//local registration
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import "@fortawesome/fontawesome-free/css/all.css";
import Home from "@/components/cc/home/Home.vue";
import UpdatesOverview from "./cc/updates/UpdatesOverview.vue";
import ServicesOverview from "./cc/ServicesOverview.vue";
import ImportValidator from "./cc/validator/ImportValidator.vue";
import ListValidator from "./cc/validator/ListValidator.vue";
import ExitValidator from "./cc/validator/ExitValidator.vue";

export default {
  name: "ControlCenterOverview",
  components: {
    Home,
    UpdatesOverview,
    ServicesOverview,
    ImportValidator,
    ListValidator,
    ExitValidator,
  },
  data() {
    return {
      content: "home",
    };
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
      this.content = "updates";
    },
    showImportValidator() {
      this.content = "importValidator";
    },
    showListValidator() {
      this.content = "listValidator";
    },
    showExitValidator() {
      this.content = "exitValidator";
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
</style>
