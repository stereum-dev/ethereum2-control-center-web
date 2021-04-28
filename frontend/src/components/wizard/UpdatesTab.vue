<template>
  <div>
    <span> Please configure unattended automized updates </span>
    <div class="text-left">
      <b-form>
        <b-form-group>
          <b-form-checkbox-group
                v-model="update.unattended"
                id="checkboxes-4">
            <b-form-checkbox value="check">Check for updates automatically</b-form-checkbox>
            <b-form-checkbox value="install" :disabled="this.update.unattended.indexOf('check') < 0">Install updates automatically</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>

        <b-form-group label="Update lane:" label-for="lane">
          <b-form-select id="lane" v-model="update.lane" :options="lanes" :disabled="this.update.unattended.indexOf('check') < 0"></b-form-select>
        </b-form-group>
      </b-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Ethereum1NodesTab",
  components: {},
  data() {
    let update = {lane: "stable", unattended: ["check", "install"]};
    this.model.updates = update;

    return {
      update: update,
      lanes: [{text: "Stable (recommended)", value: "stable"},{text: "Release Candidate (not recommmended! This can break your node!)", value: "rc"}],
    }
  },
  watch: {
    'update.lane': function(n, o) {
      this.newUrl = "https://" + this.model.network + ".infura.io:443/v3/put-your-infura-id-here";
    },
  },
  methods: {

  },
  props: {
    model: Object,
  },
};
</script>

<style scoped></style>
