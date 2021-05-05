<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Services</h2>
    </div>
    <div class="row">

      <b-table striped hover :items="services" :fields="fields">

        <template #cell(ste)="row">
          <b-icon-question
            font-scale="2"
            v-if="
              row.item.Labels == undefined ||
              row.item.Labels['com.docker.compose.project'] == undefined ||
              row.item.Labels['com.docker.compose.project'] != 'ethereum2-docker-compose'" />
          <b-img src="/public/ste_favicon.png" width="32" height="32" v-else />
        </template>
        
        <template #cell(name)="row">
          <div v-if="row.item.Labels == undefined || row.item.Labels['com.docker.compose.service'] == undefined">
            {{ row.item.Names }}
          </div>
          <div v-else>
            {{ row.item.Labels['com.docker.compose.service'] }}
          </div>
        </template>
        
        <template #cell(image)="row">
          <p>{{ row.item.Image }}</p>
        </template>
        
        <template #cell(state)="row">
          <b-icon icon="exclamation-diamond"
            variant="danger"
            font-scale="2"
            v-b-tooltip.hover
            title="Stopped"
            v-if="row.item.State === 'Exited'" />
          <b-icon icon="emoji-smile"
            variant="success"
            font-scale="2"
            v-b-tooltip.hover
            title="Running"
            v-else-if="row.item.State === 'Started'" />
          <b-icon icon="question-diamond"
            variant="warning"
            font-scale="2"
            v-b-tooltip.hover
            title="unknown state"
            v-else />
        </template>
        
        <template #cell(actions)="row">

          <b-button
            size="sm"
            @click="startService(row)"
            variant="success"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="start service">
            <b-icon icon="caret-up" aria-hidden="true"></b-icon>
          </b-button>
          
          <b-button
            size="sm"
            @click="restartService(row)"
            variant="warning"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="restart service">
            <b-icon icon="bootstrap-reboot" aria-hidden="true"></b-icon>
          </b-button>
          
          <b-button
            size="sm"
            @click="stopService(row)"
            variant="danger"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="stop service">
            <b-icon icon="caret-down" aria-hidden="true"></b-icon>
          </b-button>
          
          <b-button
            size="sm"
            @click="showServiceLogs(row)"
            variant="info"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-tooltip.hover
            title="show logs">
            <b-icon icon="book" aria-hidden="true"></b-icon>
          </b-button>

        </template>

      </b-table>
    </div>
    <b-modal ref="service-logs-modal" title="Service Logs - " size="xl" hide-footer>
      <template #modal-title>
        Service Logs - <strong>{{ logs_service }}</strong>
      </template>
      <samp style="white-space: pre-line;">{{ logs }}</samp>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: "ServicesOverview",
  components: {
  },
  data() {
    return {
      logs: "this is a log\nand this is another line of a log\n\nmore log you know...",
      logs_service: "",
      fields: [
        {key: 'ste', sortable: false, label: '' },
        {key: 'name', sortable: false, label: "Service" },
        {key: 'image', sortable: false, label: "Image" },
        {key: 'state', sortable: false, label: "State" },
        {key: 'actions', sortable: false}
      ],
      services: [
                  {
                    "Id": "8dfafdbc3a40",
                    "Names": [
                      "/boring_feynman"
                    ],
                    "Image": "ubuntu:latest",
                    "ImageID": "d74508fb6632491cea586a1fd7d748dfc5274cd6fdfedee309ecdcbc2bf5cb82",
                    "Command": "echo 1",
                    "Created": 1367854155,
                    "State": "Started",
                    "Status": "Exit 0",
                    "Ports": [
                      {
                        "PrivatePort": 2222,
                        "PublicPort": 3333,
                        "Type": "tcp"
                      }
                    ],
                    "Labels": {
                      "com.docker.compose.service": "validator",
                      "com.docker.compose.project": "ethereum2-docker-compose",
                      "com.example.vendor": "Acme",
                      "com.example.license": "GPL",
                      "com.example.version": "1.0"
                    },
                    "SizeRw": 12288,
                    "SizeRootFs": 0,
                    "HostConfig": {
                      "NetworkMode": "default"
                    },
                    "NetworkSettings": {
                      "Networks": {
                        "bridge": {
                          "NetworkID": "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                          "EndpointID": "2cdc4edb1ded3631c81f57966563e5c8525b81121bb3706a9a9a3ae102711f3f",
                          "Gateway": "172.17.0.1",
                          "IPAddress": "172.17.0.2",
                          "IPPrefixLen": 16,
                          "IPv6Gateway": "",
                          "GlobalIPv6Address": "",
                          "GlobalIPv6PrefixLen": 0,
                          "MacAddress": "02:42:ac:11:00:02"
                        }
                      }
                    },
                    "Mounts": [
                      {
                        "Name": "fac362...80535",
                        "Source": "/data",
                        "Destination": "/data",
                        "Driver": "local",
                        "Mode": "ro,Z",
                        "RW": false,
                        "Propagation": ""
                      }
                    ]
                  },
                  {
                    "Id": "9cd87474be90",
                    "Names": [
                      "/coolName"
                    ],
                    "Image": "ubuntu:latest",
                    "ImageID": "d74508fb6632491cea586a1fd7d748dfc5274cd6fdfedee309ecdcbc2bf5cb82",
                    "Command": "echo 222222",
                    "Created": 1367854155,
                    "State": "Started",
                    "Status": "Exit 0",
                    "Ports": [],
                    "Labels": {
                      "com.docker.compose.service": "geth",
                      "com.docker.compose.project": "ethereum2-docker-compose",
                    },
                    "SizeRw": 12288,
                    "SizeRootFs": 0,
                    "HostConfig": {
                      "NetworkMode": "default"
                    },
                    "NetworkSettings": {
                      "Networks": {
                        "bridge": {
                          "NetworkID": "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                          "EndpointID": "88eaed7b37b38c2a3f0c4bc796494fdf51b270c2d22656412a2ca5d559a64d7a",
                          "Gateway": "172.17.0.1",
                          "IPAddress": "172.17.0.8",
                          "IPPrefixLen": 16,
                          "IPv6Gateway": "",
                          "GlobalIPv6Address": "",
                          "GlobalIPv6PrefixLen": 0,
                          "MacAddress": "02:42:ac:11:00:08"
                        }
                      }
                    },
                    "Mounts": []
                  },
                  {
                    "Id": "3176a2479c92",
                    "Names": [
                      "/sleepy_dog"
                    ],
                    "Image": "ubuntu:latest",
                    "ImageID": "d74508fb6632491cea586a1fd7d748dfc5274cd6fdfedee309ecdcbc2bf5cb82",
                    "Command": "echo 3333333333333333",
                    "Created": 1367854154,
                    "State": "Foobar",
                    "Status": "Exit 0",
                    "Ports": [],
                    "Labels": {
                      "com.docker.compose.service": "beacon",
                      "com.docker.compose.project": "ethereum2-docker-compose",
                    },
                    "SizeRw": 12288,
                    "SizeRootFs": 0,
                    "HostConfig": {
                      "NetworkMode": "default"
                    },
                    "NetworkSettings": {
                      "Networks": {
                        "bridge": {
                          "NetworkID": "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                          "EndpointID": "8b27c041c30326d59cd6e6f510d4f8d1d570a228466f956edf7815508f78e30d",
                          "Gateway": "172.17.0.1",
                          "IPAddress": "172.17.0.6",
                          "IPPrefixLen": 16,
                          "IPv6Gateway": "",
                          "GlobalIPv6Address": "",
                          "GlobalIPv6PrefixLen": 0,
                          "MacAddress": "02:42:ac:11:00:06"
                        }
                      }
                    },
                    "Mounts": []
                  },
                  {
                    "Id": "4cb07b47f9fb",
                    "Names": [
                      "/running_cat"
                    ],
                    "Image": "ubuntu:latest",
                    "ImageID": "d74508fb6632491cea586a1fd7d748dfc5274cd6fdfedee309ecdcbc2bf5cb82",
                    "Command": "echo 444444444444444444444444444444444",
                    "Created": 1367854152,
                    "State": "Exited",
                    "Status": "Exit 0",
                    "Ports": [],
                    "Labels": {},
                    "SizeRw": 12288,
                    "SizeRootFs": 0,
                    "HostConfig": {
                      "NetworkMode": "default"
                    },
                    "NetworkSettings": {
                      "Networks": {
                        "bridge": {
                          "NetworkID": "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                          "EndpointID": "d91c7b2f0644403d7ef3095985ea0e2370325cd2332ff3a3225c4247328e66e9",
                          "Gateway": "172.17.0.1",
                          "IPAddress": "172.17.0.5",
                          "IPPrefixLen": 16,
                          "IPv6Gateway": "",
                          "GlobalIPv6Address": "",
                          "GlobalIPv6PrefixLen": 0,
                          "MacAddress": "02:42:ac:11:00:05"
                        }
                      }
                    },
                    "Mounts": []
                  }
                ],
    };
  },
  props: {
    ethereum2config: Object,
  },
  methods: {
    startService(row) {

    },
    restartService(row) {

    },
    stopService(row) {

    },
    showServiceLogs(row) {
      if (row.item.Labels == undefined || row.item.Labels['com.docker.compose.service'] == undefined) {
        this.logs_service = row.item.Names;
      } else {
        this.logs_service = row.item.Labels['com.docker.compose.service'];
      }

      // todo: fill log var:
      // this.logs = call_ansible(row.item.Id);

      this.$refs['service-logs-modal'].show();
    },
  }
};
</script>

<style scoped></style>
