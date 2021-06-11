<template>
  <div class="container">
    <div class="row pb-3 pt-3 text-left">
      <div class="col-6">
        <h2>Services</h2>
      </div>
      <div class="col-6 text-right">
        <b-button variant="success" @click="refreshServices">
          <b-icon icon="arrow-clockwise" aria-hidden="true"></b-icon>
          Refresh
        </b-button>
      </div>
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

          <b-button
            size="sm"
            @click="showServicePorts(row)"
            variant="info"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="show ports"
            :disabled="Object.entries(containers[row.item]).length == 0 || !containers[row.item][Object.keys(containers[row.item])[0]].state.running"
          >
            <b-icon icon="diagram3" aria-hidden="true"></b-icon>
            <!--
            <b-icon icon="signpost-split" aria-hidden="true"></b-icon>
            -->
          </b-button>
        </template>
      </b-table>
    </div>

    <b-modal
      ref="service-logs-modal"
      title="Service Logs - "
      size="xl"
      hide-footer
    >
      <template #modal-title>
        Service Logs - <strong>{{ logs_service }}</strong>
      </template>
      <samp style="white-space: pre-line; font-size: 10px;">{{ logs }}</samp>
    </b-modal>

    <b-modal
      ref="service-ports-modal"
      title="Service Ports - "
      size="m"
      hide-footer
    >
      <template #modal-title>
        Service Ports - <strong>{{ logs_service }}</strong>
      </template>
      <b-table striped hover :items="ports" :fields="port_fields" v-if="Array.isArray(ports)">
        <template #cell(ip)="row">
          <div v-if="typeof row.item.IP === 'undefined'">
            not listening
          </div>
          <div v-else>
            {{ row.item.IP }}
          </div>
        </template>

        <template #cell(internal)="row">
          <div>
            {{ row.item.PrivatePort }}
          </div>
        </template>

        <template #cell(external)="row">
          <div v-if="typeof row.item.PublicPort === 'undefined'">
            no port set
          </div>
          <div v-else>
            {{ row.item.PublicPort }}
          </div>
        </template>

        <template #cell(tcpudp)="row">
          <div>
            {{ row.item.Type }}
          </div>
        </template>
      </b-table>
    </b-modal>
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
      logs: "",
      logs_service: "",
      ports: "",
      ports_service_name: "",
      port_fields: [
        { key: "ip", sortable: false, label: "Binding IP" },
        { key: "internal", sortable: false, label: "Port on Service" },
        { key: "external", sortable: false, label: "Port on Host" },
        { key: "tcpudp", sortable: false, label: "Type" },
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
      this.logs_service = row.item;
      this.readData("service-logs", { stereum_service: Object.keys(this.containers[row.item])[0]}, this.refreshLogsModel);
    },
    showServicePorts(row) {
      this.logs_service = row.item;
      this.ports_service_name = Object.keys(this.containers[row.item])[0];

      this.readData("read-ports", {}, this.refreshPortsModel);
    },

    refreshServices: function() {
      this.readData("read-services", {}, this.refreshServicesModel);
    },

    refreshServicesModel() {
      this.containers = this.processStatus.logs.tasks[1].message.services;
    },

    refreshLogsModel() {
      if (this.processStatus.logs.tasks[1].message.stdout) {
        this.logs = this.processStatus.logs.tasks[1].message.stdout;
      } else {
        this.logs = this.processStatus.logs.tasks[1].message.stderr;
      }

      this.$refs["service-logs-modal"].show();
    },

    refreshPortsModel() {
      this.ports = [];
      for (let container of this.processStatus.logs.tasks[1].message.containers) {
        for (let nameLabel of container.Names) {
          if (nameLabel.includes(this.ports_service_name)) {
            this.ports = container.Ports;
          }
        }
      }

      this.$refs["service-ports-modal"].show();
    }
  },
};
</script>

<style scoped></style>
