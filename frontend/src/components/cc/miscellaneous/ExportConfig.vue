<template>
  <div class="container">
    <div class="row pb-3 pt-3">
      <h2>Export Configuration</h2>
    </div>
    <div class="col-12 text-left">
      <span>The configuration which is currently running on your device will be exported and stored in "/tmp/exported-config.zip"</span>
    </div>
    <div class="container pb-3 pt-3">
      <p class="text-left">
        <b-form inline>
          <label class="mb-2 mr-sm-2 mb-sm-0" for="inline-new-url">
            Exported file's Password:
          </label>
          <b-form-input
            v-model="password"
            type="password"
            placeholder="Exported file's password"
            align="left"
            class="mb-2 mr-sm-2 mb-sm-0 w-50"
          />

          <b-button
            variant="primary"
            @click="exportConfig"
            :disabled="password.length === 0"
            title="ExportConfig"
          >
            Export Config
          </b-button>
        </b-form>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExportConfig",
  components: {},
  data() {
    return {
      password: "",
    };
  },
  props: {
    model: Object,
    processChange: Function,
  },
  methods: {
    exportConfig() {
      this.processChange("export-config", 100, {
          export_config_password: this.password,
      });
    },
  },
};
</script>

<style scoped></style>
