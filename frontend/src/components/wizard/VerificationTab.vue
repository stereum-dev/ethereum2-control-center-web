<template>
  <div>
    <span v-if="!running">
      Please check the entered information and start the installation
    </span>
    <span v-if="running">
      <b>Installation in Progress, please be patient</b>
    </span>
    <data>
      <table class="text-left table">
        <tr>
          <td class="table-label">Network:</td> 
          <td class="table-data">{{ model.network }}</td>
        </tr>
        <tr>
          <td class="table-label">Client:</td> 
          <td class="table-data">{{ model.client }}</td>
        </tr>
        <tr>
          <td class="table-label">Installation Folder:</td> 
          <td class="table-data">{{ model.installationFolder }}</td>
        </tr>
      </table>

      <div v-if="running">
        <b-progress :value="progress" variant="info" :max="max" show-progress animated>
          <b-progress-bar :value="progress">
            <span>Progress: <strong>{{ progress.toFixed(0) }}%</strong></span>
          </b-progress-bar>
        </b-progress>
      </div>
    </data>
  </div>
</template>

<script>

export default {
  name: "VerificationTab",
  components: {    
  },
  props: {    
    model: Object,
    running: Boolean,
    progress: Number,
  },
  data () {
    return {
      max: 100,      
    }
  },
  methods: {    
  }
};
</script>

<style scoped>  
</style>
