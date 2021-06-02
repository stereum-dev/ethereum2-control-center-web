<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Service Port List</h2>
    </div>
    <div class="row">
      <b-table striped hover :items="services" :fields="fields">
        <template #cell(ste)="row">
          <b-icon-question
            font-scale="2"
            v-if="
              row.item.Labels == undefined ||
              row.item.Labels['com.docker.compose.project'] == undefined ||
              row.item.Labels['com.docker.compose.project'] !=
                'ethereum2-docker-compose'
            "
          />
          <b-img src="/public/ste_favicon.png" width="32" height="32" v-else />
        </template>

        <template #cell(service)="row">
           <p> {{ row.item.Names }}</p>
        </template>

        <template #cell(port)="row">
          <p>{{ row.item.Ports }}</p>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "PortList",
  components: {},
  data() {
    return {
      fields: [
        { key: "ste", sortable: false, label: "" },
        { key: "service", sortable: false, label: "Services" },
        { key: "port", sortable: false, label: "Port/TCP" },
      ],
      services: [
        {
          Names: "Validator",
          Ports: "5052",
          Labels: {
            "com.docker.compose.project": "ethereum2-docker-compose",
          },
        },
        {
          Names: "Beacon",
          Ports: "1234",
          Labels: {
            "com.docker.compose.project": "ethereum2-docker-compose",
          },
        },
        {
          Names: "Grafana",
          Ports: "3000",
          Labels: {
            "com.docker.compose.project": "ethereum2-docker-compose",
          },
        },
        {
          Names: "Prometheus",
          Ports: "9000",
        },
      ],
    };
  },
  props: {
    ethereum2config: Object,
  },
  methods: {
  },
};
</script>

<style scoped></style>
