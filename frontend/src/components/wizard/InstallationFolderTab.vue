<template>
  <div class="text-left">
    <h3>Installation Path</h3>
    <b-alert show variant="info">
      In this step, you can change the installation path of the Setup.
      <br/>
      By enabling Fast-Sync a blockchain database snapshot will be downloaded from Stereum cloud services and installed. This shortens the synchronization time significantly but is less secure than loading each block from genesis until now.
    </b-alert>
    <div>
      <b-form-input
        v-model="model.installationFolder"
        placeholder="Enter installation path"
        :state="validation"
      ></b-form-input>
    </div>

    <b-form-checkbox v-if="this.model.importConfig == false" v-model="model.fastSync" name="fastSync" switch>
      Fast-Sync
    </b-form-checkbox>

    <b-alert 
      v-if="spaceLeft >= 900"
      show
      variant="success"
      class="mt-3"
      >Space left on the partition of this path: {{ spaceLeft }} gb (recommended: 900 gb)
    </b-alert>
    <b-alert 
      v-else
      show
      variant="danger"
      class="mt-3"
      >Space left on the partition of this path: {{ spaceLeft }} gb (recommended: 900 gb)
    </b-alert>
  </div>
</template>

<script>
export default {
  name: "InstallationFolderTab",
  components: {},
  data() {
    return {
      spaceLeft: 0,
    };
  },
  props: {
    model: Object,
    ansibleFacts: Object,
  },
  computed: {
    validation() {
      this.spaceLeft = 0;
      var pathLength = 0;

      if (this.ansibleFacts !== undefined) {
        for (let mount of this.ansibleFacts.mounts) {
          if (this.model.installationFolder.startsWith(mount.mount) && pathLength < mount.mount.length) {
            pathLength = mount.mount.length;
            this.spaceLeft = Math.round(mount.size_available / 1024 / 1024 / 1024);
          }
        }
      }

      return this.model.installationFolder.length > 0 && this.model.installationFolder.startsWith("/");
    },
  },
};
</script>

<style scoped></style>
