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

        <template #cell(sync)="row">
          <div>
            <vue-ellipse-progress 
              v-if="row.item.includes('beacon')"
              :size="32"
              :color="sync_data[row.item].syncColor"
              :thickness="5"
              :legend="false"
              :progress="sync_data[row.item].syncProgress"
              :loading="sync_data[row.item].syncLoading"
              :noData="sync_data[row.item].syncNoData"
              :emptyColor="sync_data[row.item].syncEmptyColor"
              v-b-tooltip.hover
              :title="sync_data[row.item].title"
              />
          </div>
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
import axios from "axios";

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
        { key: "sync", sortable: false, label: "Sync" },
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
      sync_data: {},
      sync_port_map: {
        "lighthouse_beacon": 5052,
        "lodestar_beacon": 9596,
        "nimbus_beacon": 5052,
        "prysm_beacon": 3501,
        "prysm_beacon_slasher": 3501,
        "teku_beacon": 5051,
      },
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
      const allServices = this.processStatus.logs.tasks[1].message.services;
      const allContainers = Object.keys(allServices).sort();

      const filteredContainers = [];
      for (const container of allContainers) {
        if (
          allServices[container][Object.keys(allServices[container])[0]] === undefined ||
          (
            allServices[container][Object.keys(allServices[container])[0]].image != "tianon/true" &&
            Object.entries(allServices[container]).length > 0
          )
          ) {
          console.log("keeping " + container);

          if (container.includes('beacon')) {
            const service = allServices[container][Object.keys(allServices[container])[0]];

            if (this.ethereum2config.setup == 'prysm') {
              this.refreshSyncModel(container, 3501);
            } else if (this.ethereum2config.setup == 'lighthouse') {
              this.refreshSyncModel(container, 5052);
            } else if (this.ethereum2config.setup == 'nimbus') {
              this.refreshSyncModel(container, 5052);
            } else if (this.ethereum2config.setup == 'lodestar') {
              this.refreshSyncModel(container, 9596);
            } else if (this.ethereum2config.setup == 'teku' ) {
              this.refreshSyncModel(container, 5051);
            } else if (this.ethereum2config.setup == 'allbeacons' ) {
              this.refreshSyncModel(container, this.sync_port_map[container]);
            } else if (this.ethereum2config.setup == 'multiclient' ) {
              this.refreshSyncModel(container, this.sync_port_map[container]);
            }
          }
        } else {
          delete allServices[container];
        }
      }

      this.containers = allServices
    },

    refreshSyncModel(container, port) {
      this.sync_data[container] = {
        syncLoading: true,
        syncNoData: false,
        syncEmptyColor: "#8ec5fc",
        syncProgress: 60,
        syncColor: "lightblue",
        title: "Loading..."
      };

      const beaconServiceHost = container + ":" + port;
      console.log("query with service: " + beaconServiceHost);

      axios
        .post("/api/ethereum", {
          "service": beaconServiceHost,
          "uri": "/eth/v1/node/syncing",
          "method": "GET",
          "content": {}
        })
        .then((response) => {
          console.log(response.data);
          this.sync_data[container].syncLoading = false;
          if (!response.data.data.is_syncing) {
            this.sync_data[container].syncProgress = 100;
            this.sync_data[container].syncColor = "ForestGreen";
            this.sync_data[container].title = "Fully synced at block " + parseInt(response.data.data.head_slot);
          } else {
            const progress = parseInt(response.data.data.head_slot) / (parseInt(response.data.data.head_slot) + parseInt(response.data.data.sync_distance)) * 100;
            console.log("progress for " + container + ": " + progress);
            this.sync_data[container].syncProgress = progress;
            this.sync_data[container].syncColor = "SteelBlue";
            this.sync_data[container].title = "Syncing " + parseInt(response.data.data.head_slot) + "/" + (parseInt(response.data.data.head_slot) + parseInt(response.data.data.sync_distance)) + " (" + Math.round(progress) + " %)";
          }
          this.$forceUpdate();
        })
        .catch((error) => {
          console.log(error);
          this.sync_data[container].syncLoading = false;
          this.sync_data[container].syncNoData = true;
          this.sync_data[container].syncEmptyColor = "red";
          this.sync_data[container].title = "Can't read sync status";
          this.$forceUpdate();
        });
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
