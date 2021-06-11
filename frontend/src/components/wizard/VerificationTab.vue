<template>
  <div class="text-left">
    <h3>Verify &amp; Install</h3>
    <span v-if="!running">
      Please check the entered information and start the installation
    </span>
    <data>
      <div v-if="!running || done">
        <table class="text-left table">
          <tr>
            <td class="table-label">Network:</td>
            <td class="table-data">{{ model.network }}</td>
          </tr>
          <tr>
            <td class="table-label">Setup:</td>
            <td class="table-data">{{ model.client }}</td>
          </tr>
          <tr>
            <td class="table-label">Customization:</td>
            <td class="table-data">{{ model.override }}</td>
          </tr>
          <tr>
            <td class="table-label">Ethereum 1 nodes:</td>
            <td class="table-data">
              <!--
              <b-table striped hover :items="model.eth1nodes"> </b-table>
              -->
              <li v-for="eth1node in model.eth1nodes" :key="eth1node">
                {{ eth1node }}
              </li>
            </td>
          </tr>
          <tr>
            <td class="table-label">Updates:</td>
            <td class="table-data">
              <div
                v-if="
                  !(typeof model.updates.unattended === 'undefined') &&
                  model.updates.unattended.indexOf('check') > -1
                "
              >
                Check for updates automatically: <strong>Yes</strong>
                <br />Unattended update installation:
                <strong v-if="model.updates.unattended.indexOf('install') > -1"
                  >Yes</strong
                ><strong v-else>No</strong> <br />Lane:
                <strong>{{ model.updates.lane }}</strong>
              </div>
              <div v-else>Check for updates: <strong>No</strong></div>
            </td>
          </tr>
          <tr>
            <td class="table-label">Installation Folder:</td>
            <td class="table-data">{{ model.installationFolder }}</td>
          </tr>
        </table>
      </div>

      <div v-if="running || done">
        <div v-if="running">
          <div class="alert alert-primary" role="alert">
            <b>Installation in Progress, please be patient</b>&nbsp;<i
              class="fas fa-cog fa-spin"
            ></i>
            <div>
              <b-progress
                :value="progress"
                variant="info"
                :max="max"
                show-progress
                animated
              >
                <b-progress-bar :value="progress">
                  <span
                    >Progress: <strong>{{ progress.toFixed(0) }}%</strong></span
                  >
                </b-progress-bar>
              </b-progress>
            </div>
          </div>
        </div>

        <div v-if="success === true">
          <div class="alert alert-success" role="alert">
            <h4 class="alert-heading">Installation Successful! You are good to go!</h4>

            <b-button variant="primary" block size="lg" href="http://localhost:8081/public/control-center">Open Control Center</b-button>
          </div>
        </div>
        <div v-if="success === false">
          <div class="alert alert-danger" role="alert">
            Unfortunately the Installation failed, please consult logs for
            details
          </div>
        </div>

        <ul class="list-group list-unstyled">
          <task-status-entry
            class="list-group-item text-left"
            v-bind:key="index"
            v-for="(status, index) in logs"
            :model="status"
          ></task-status-entry>
        </ul>
      </div>
    </data>
  </div>
</template>

<script>
import TaskStatusEntry from "@/components/commons/TaskStatusEntry.vue";

export default {
  name: "VerificationTab",
  components: {
    TaskStatusEntry,
  },
  props: {
    model: Object,
    running: Boolean,
    success: Boolean,
    done: Boolean,
    progress: Number,
    logs: Array,
  },
  data() {
    return {
      max: 62,
    };
  },
  methods: {},
};
</script>

<style scoped>
.alert-primary {
  color: #fff;
  background-color: rgb(51, 102, 102);
  border-color: rgb(51, 102, 102);
}
</style>
