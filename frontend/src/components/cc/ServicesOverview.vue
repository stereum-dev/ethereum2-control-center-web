<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Services</h2>
    </div>
    <div class="row">
      <b-table striped hover :items="Object.keys(containers).sort()" :fields="fields" v-if="Object.entries(containers).length > 0">

        <template #cell(ste)="row">
          <b-img src="/public/ste_favicon.png" width="32" height="32" />
        </template>

        <template #cell(name)="row">
          <div>
            {{ row.item }}
          </div>
        </template>


        <template #cell(image)="row">
          <p v-if="Object.entries(containers[row.item]).length == 0">unknown</p>
          <p v-else>{{ containers[row.item][Object.keys(containers[row.item])[0]].image }}</p>
        </template>


        <template #cell(state)="row">
          <b-icon
            icon="emoji-smile"
            variant="success"
            font-scale="2"
            v-b-tooltip.hover
            title="Running"
            v-if="Object.entries(containers[row.item]).length > 0 && containers[row.item][Object.keys(containers[row.item])[0]].state.running"
          />
          <b-icon
            icon="exclamation-diamond"
            variant="danger"
            font-scale="2"
            v-b-tooltip.hover
            title="Stopped"
            v-else
          />
        </template>

        <template #cell(actions)="row">
          <b-button
            size="sm"
            @click="startService(row)"
            variant="success"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="start service"
            :disabled="Object.entries(containers[row.item]).length > 0 && containers[row.item][Object.keys(containers[row.item])[0]].state.running"
          >
            <b-icon icon="caret-up" aria-hidden="true"></b-icon>
          </b-button>

          <b-button
            size="sm"
            @click="restartService(row)"
            variant="warning"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="restart service"
            :disabled="Object.entries(containers[row.item]).length == 0 || !containers[row.item][Object.keys(containers[row.item])[0]].state.running"
          >
            <b-icon icon="bootstrap-reboot" aria-hidden="true"></b-icon>
          </b-button>

          <b-button
            size="sm"
            @click="stopService(row)"
            variant="danger"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="stop service"
            :disabled="Object.entries(containers[row.item]).length == 0 || !containers[row.item][Object.keys(containers[row.item])[0]].state.running"
          >
            <b-icon icon="caret-down" aria-hidden="true"></b-icon>
          </b-button>

          <b-button
            size="sm"
            @click="showServiceLogs(row)"
            variant="info"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="show logs"
            :disabled="Object.entries(containers[row.item]).length == 0"
          >
            <b-icon icon="book" aria-hidden="true"></b-icon>
          </b-button>
        </template>
      </b-table>
    </div>
    <!--
    <b-modal
      ref="service-logs-modal"
      title="Service Logs - "
      size="xl"
      hide-footer
    >
      <template #modal-title>
        Service Logs - <strong>{{ logs_service }}</strong>
      </template>
      <samp style="white-space: pre-line">{{ logs }}</samp>
    </b-modal>
    -->
  </div>
</template>

<script>
export default {
  name: "ServicesOverview",
  components: {},
  data() {
    return {
      containers: {},
      fields: [
        { key: "ste", sortable: false, label: "" },
        { key: "name", sortable: false, label: "Service" },
        { key: "image", sortable: false, label: "Image" },
        { key: "state", sortable: false, label: "State" },
        { key: "actions", sortable: false },
      ],
    };
  },
  created() {
    this.refreshServices();
  },
  props: {
    ethereum2config: Object,
    processStatus: Object,
    readData: Function,
  },
  methods: {
    startService(row) {
      this.readData("start-service", { stereum_service: row.item}, this.refreshServicesModel);
    },
    restartService(row) {
      this.readData("restart-service", { stereum_service: row.item}, this.refreshServicesModel);
    },
    stopService(row) {
      this.readData("stop-service", { stereum_service: row.item}, this.refreshServicesModel);
    },
    showServiceLogs(row) {
      if (
        row.item.Labels == undefined ||
        row.item.Labels["com.docker.compose.service"] == undefined
      ) {
        this.logs_service = row.item.Names;
      } else {
        this.logs_service = row.item.Labels["com.docker.compose.service"];
      }

      // todo: fill log var:
      // this.logs = call_ansible(row.item.Id);

      this.$refs["service-logs-modal"].show();
    },

    refreshServices: function() {
      this.readData("read-services", {}, this.refreshServicesModel);
    },

    refreshServicesModel() {
      this.containers = this.processStatus.logs.tasks[1].message.services;
    },
  },
};
</script>

<style scoped></style>
