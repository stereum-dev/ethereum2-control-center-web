<template>
    <div class="text-left">
        <b-form>
        <b-form-group>
            <b-form-checkbox-group
                v-model="update.unattended">
            <b-form-checkbox value="check">Check for updates automatically</b-form-checkbox>
            <b-form-checkbox value="install" :disabled="this.update.unattended.indexOf('check') < 0">Install updates automatically</b-form-checkbox>
            </b-form-checkbox-group>
        </b-form-group>

        <b-form-group label="Update lane:" label-for="lane">
            <b-form-select id="lane" v-model="update.lane" :options="lanes" :disabled="this.update.unattended.indexOf('check') < 0"></b-form-select>
        </b-form-group>
        </b-form>
    </div>
</template>

<script>
export default {
  name: "UpdatesConfiguration",
  components: {},
  data() {
    let updates;
    if (!(this.ethereum2config.updates === undefined) && !(this.ethereum2config.updates.unattended === undefined)) {
        updates = this.ethereum2config.updates;
    } else {
        updates = {lane: "stable", unattended: ["check", "install"]};
        this.ethereum2config.updates = updates;
    }

    return {
      update: updates,
      lanes: [{text: "Stable (recommended)", value: "stable"},{text: "Release Candidate (not recommmended! This can break your node!)", value: "rc"}],
    }
  },
  watch: {
    'update.lane': function(n, o) {
      this.newUrl = "https://" + this.ethereum2config.network + ".infura.io:443/v3/put-your-infura-id-here";
    },
  },
  methods: {

  },
  props: {
    ethereum2config: Object,
  },
};
</script>

<style scoped></style>
