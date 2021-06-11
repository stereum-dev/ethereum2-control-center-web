<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Validators</h2>
    </div>

    <div class="row">
      <div class="alert alert-info" role="alert">
        <p>
          For a list of validators please visit the link below! A list with your validators in the Stereum Control Center with various controls will follow soon.
        </p>

        <b-button
          v-if="this.ethereum2config.override !== 'beacon-validator' && this.ethereum2config.setup !== 'allbeacons'"
          variant="primary"
          block
          size="lg"
          href="http://localhost:8082"
        >Open Grafana</b-button>
        <b-button
          v-if="this.ethereum2config.setup === 'prysm'"
          variant="primary"
          block
          size="lg"
          href="http://localhost:8083"
        >Open Prysm UI</b-button>
      </div>
    </div>

    <div class="row" v-if="false">
      <b-table striped hover :items="validators" :fields="fields">
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

        <template #cell(pubkey)="row">
          <div
            v-if="
              row.item.Labels == undefined ||
              row.item.Labels['com.docker.compose.pubkey'] == undefined
            "
          >
            {{ row.item.Names }}
          </div>
          <div v-else>
            {{ row.item.Labels["com.docker.compose.pubkey"] }}
          </div>
        </template>

        <template #cell(balance)="row">
          <p>{{ row.item.Balance }}</p>
        </template>

        <template #cell(state)="row">
          <b-icon-check-square
            variant="success"
            font-scale="2"
            v-b-icon-check-square.hover
            title="Active"
            v-if="row.item.State === 'Active'"
          />
          <b-icon-dash-square
            variant="danger"
            font-scale="2"
            v-b-icon-dash-square.hover
            title="Inactive"
            v-else-if="row.item.State === 'Inactive'"
          />
          <b-icon-box-arrow-right
            variant="secondary"
            font-scale="2"
            v-icon-box-arrow-right.hover
            title="Exited"
            v-else-if="row.item.State === 'Exited'"
          />
          <b-icon-question-square
            variant="warning"
            font-scale="2"
            v-icon-question-square.hover
            title="Unknown state"
            v-else
          />
        </template>

        <template #cell(actions)="row">
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
            @click="openBeaconcha()"
            variant="primary"
            class="mb-2 mr-sm-2 mb-sm-0"
            v-b-link.hover
            title="go to https://beaconcha.in"
          >
            <b-icon icon="link" aria-hidden="true"></b-icon>
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
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "ListValidator",
  components: {},
  data() {
    return {
      fields: [
        { key: "ste", sortable: false, label: "" },
        { key: "pubkey", sortable: false, label: "Validator public key" },
        { key: "balance", sortable: false, label: "Balance" },
        { key: "state", sortable: false, label: "State" },
        { key: "actions", sortable: false },
      ],
      validators: [
        {
          Id: "8dfafdbc3a40",
          Names: ["/boring_feynman"],
          Balance: "32.00032 ETH",
          Image: "ubuntu:latest",
          ImageID:
            "d74508fb6632491cea586a1fd7d748dfc5274cd6fdfedee309ecdcbc2bf5cb82",
          Command: "echo 1",
          Created: 1367854155,
          State: "Active",
          Status: "Exit 0",
          Ports: [
            {
              PrivatePort: 2222,
              PublicPort: 3333,
              Type: "tcp",
            },
          ],
          Labels: {
            "com.docker.compose.pubkey": "0x123456789...",
            "com.docker.compose.project": "ethereum2-docker-compose",
            "com.example.vendor": "Acme",
            "com.example.license": "GPL",
            "com.example.version": "1.0",
          },
          SizeRw: 12288,
          SizeRootFs: 0,
          HostConfig: {
            NetworkMode: "default",
          },
          NetworkSettings: {
            Networks: {
              bridge: {
                NetworkID:
                  "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                EndpointID:
                  "2cdc4edb1ded3631c81f57966563e5c8525b81121bb3706a9a9a3ae102711f3f",
                Gateway: "172.17.0.1",
                IPAddress: "172.17.0.2",
                IPPrefixLen: 16,
                IPv6Gateway: "",
                GlobalIPv6Address: "",
                GlobalIPv6PrefixLen: 0,
                MacAddress: "02:42:ac:11:00:02",
              },
            },
          },
          Mounts: [
            {
              Name: "fac362...80535",
              Source: "/data",
              Destination: "/data",
              Driver: "local",
              Mode: "ro,Z",
              RW: false,
              Propagation: "",
            },
          ],
        },
        {
          Id: "9cd87474be90",
          Names: ["/coolName"],
          Balance: "33.0009868 ETH",
          Image: "ubuntu:latest",
          ImageID:
            "d74508fb6632491cea586a1fd7d748dfc5274cd6fdfedee309ecdcbc2bf5cb82",
          Command: "echo 222222",
          Created: 1367854155,
          State: "Inactive",
          Status: "Exit 0",
          Ports: [],
          Labels: {
            "com.docker.compose.pubkey": "0x586745849...",
            "com.docker.compose.project": "ethereum2-docker-compose",
          },
          SizeRw: 12288,
          SizeRootFs: 0,
          HostConfig: {
            NetworkMode: "default",
          },
          NetworkSettings: {
            Networks: {
              bridge: {
                NetworkID:
                  "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                EndpointID:
                  "88eaed7b37b38c2a3f0c4bc796494fdf51b270c2d22656412a2ca5d559a64d7a",
                Gateway: "172.17.0.1",
                IPAddress: "172.17.0.8",
                IPPrefixLen: 16,
                IPv6Gateway: "",
                GlobalIPv6Address: "",
                GlobalIPv6PrefixLen: 0,
                MacAddress: "02:42:ac:11:00:08",
              },
            },
          },
          Mounts: [],
        },
        {
          Id: "3176a2479c92",
          Names: ["/sleepy_dog"],
          Balance: "32.00005 ETH",
          Image: "ubuntu:latest",
          ImageID:
            "d74508fb6632491cea586a1fd7d748dfc5274cd6fdfedee309ecdcbc2bf5cb82",
          Command: "echo 3333333333333333",
          Created: 1367854154,
          State: "Exited",
          Status: "Exit 0",
          Ports: [],
          Labels: {
            "com.docker.compose.pubkey": "0x758493765...",
            "com.docker.compose.project": "ethereum2-docker-compose",
          },
          SizeRw: 12288,
          SizeRootFs: 0,
          HostConfig: {
            NetworkMode: "default",
          },
          NetworkSettings: {
            Networks: {
              bridge: {
                NetworkID:
                  "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                EndpointID:
                  "8b27c041c30326d59cd6e6f510d4f8d1d570a228466f956edf7815508f78e30d",
                Gateway: "172.17.0.1",
                IPAddress: "172.17.0.6",
                IPPrefixLen: 16,
                IPv6Gateway: "",
                GlobalIPv6Address: "",
                GlobalIPv6PrefixLen: 0,
                MacAddress: "02:42:ac:11:00:06",
              },
            },
          },
          Mounts: [],
        },
        {
          Id: "4cb07b47f9fb",
          Names: ["/running_cat"],
          Balance: "34.000456 ETH",
          Image: "ubuntu:latest",
          ImageID:
            "d74508fb6632491cea586a1fd7d748dfc5274cd6fdfedee309ecdcbc2bf5cb82",
          Command: "echo 444444444444444444444444444444444",
          Created: 1367854152,
          State: "Unknown..",
          Status: "Exit 0",
          Ports: [],
          Labels: {},
          SizeRw: 12288,
          SizeRootFs: 0,
          HostConfig: {
            NetworkMode: "default",
          },
          NetworkSettings: {
            Networks: {
              bridge: {
                NetworkID:
                  "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                EndpointID:
                  "d91c7b2f0644403d7ef3095985ea0e2370325cd2332ff3a3225c4247328e66e9",
                Gateway: "172.17.0.1",
                IPAddress: "172.17.0.5",
                IPPrefixLen: 16,
                IPv6Gateway: "",
                GlobalIPv6Address: "",
                GlobalIPv6PrefixLen: 0,
                MacAddress: "02:42:ac:11:00:05",
              },
            },
          },
          Mounts: [],
        },
      ],
    };
  },
  props: {
    ethereum2config: Object,
  },
  methods: {
    openBeaconcha: function () {
      window.open("https://beaconcha.in/", "_blank");
    },
    exitValidator() {},
    removeValidator() {},
  },
};
</script>

<style scoped></style>
