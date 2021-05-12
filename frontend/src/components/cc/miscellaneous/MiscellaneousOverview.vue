<template>
  <div class="mt-3 mr-5 ml-5 mb-3">
    <b-card-group columns>
      <b-card
        title="Graffiti"
        style="max-width: 20rem;">
        <b-card-text>
          Set a mark on the beacon chain by choosing your own graffiti. This text will be included in every block your validator keys are propsing and visible for everybody!
        </b-card-text>

        <b-button @click="this.showGraffiti" variant="primary">Set Graffiti</b-button>
      </b-card>
      <b-card
        title="API Bind Address"
        sub-title="Expert Only"
        style="max-width: 20rem;">
        <b-card-text>
          If you want to use your beacon client(s) or monitoring to be accessible outside of your server, configure on which IP the services should listen on.
        </b-card-text>

        <b-button @click="this.showApiBindAddress" variant="primary">Set API Bind Address</b-button>
      </b-card>
      <b-card
        title="Geth Prune"
        style="max-width: 20rem;">
        <b-card-text>
          Geth is the Ethereum 1 client. It's collecting lots of data and some of it can be deleted again after some days. Run this to fee up some storage space again!
        </b-card-text>

        <b-button href="#" variant="primary">Prune Geth Now</b-button>
      </b-card>
      <b-card
        title="Restart Host"
        style="max-width: 20rem;">
        <b-card-text>
          Sometimes there are things getting stuck or not responding anmore, a restart might help you resolve some issues (but not all). Keep in mind it might take a couple of minutes.
        </b-card-text>

        <b-button href="#" variant="primary">Restart Now</b-button>
      </b-card>
      <b-card
        title="Service Port List"
        style="max-width: 20rem;">
        <b-card-text>
          This shows you the ports used by your Stereum Ethereum Node Setup. Might come in handy when configuring your firewall and setting up port forwards. This is view-only.
        </b-card-text>

        <b-button href="#" variant="primary">Show Port List</b-button>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>

export default {
  name: "MiscellaneousOverview",
  components: {
  },
  data() {
    return {};
  },
  props: {
    ethereum2config: Object,
    showGraffiti: Function,
    showApiBindAddress: Function,
  },
  methods: {
  },
};
</script>

<style scoped>
.card {
  margin: 0 auto; /* Added */
  float: none; /* Added */
  margin-bottom: 10px; /* Added */
}
</style>
