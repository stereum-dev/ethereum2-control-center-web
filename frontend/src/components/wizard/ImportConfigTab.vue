<template>
  <div class="text-left">
    <h3>Import Configuration</h3>
    <b-alert show variant="info">
      The exported configuration file (exported-config.zip) could be imported here. The node will be configured as exported setup.  
    </b-alert>
    
    <div class="col-8">
      <b-form-checkbox 
      v-model="model.importConfig" 
      name="importConfig" 
      @change="clearConfigData"
      switch
      >
        Import Configuration
      </b-form-checkbox>
    
      <b-form-input
        v-model="model.exportedConfigFolder"
        placeholder="Enter exported-config file's path (e. g: /tmp/exported-config.zip)"
        :state="validateConfigFolder"
        :disabled="this.model.importConfig == false"
      ></b-form-input>
      <b-form-input
        v-model="model.configPassword"
        placeholder="Enter exported-config file's password"
        type="password"
        :state="validateConfigPassword"
        :disabled="this.model.importConfig == false"
      ></b-form-input>
    
      <b-form-checkbox
        v-model="model.importValidator" 
        name="importValidator" 
        @change="clearValidatorData"
        :disabled="this.model.importConfig == false"
        switch
        >
        Import Validators
      </b-form-checkbox>
      <b-form-input
        v-model="model.validatorPassword"
        placeholder="Enter validator's password"
        type="password"
        :state="validateValidatorPassword"
        :disabled="this.model.importValidator == false || this.model.importConfig == false"
      ></b-form-input>
    </div>
  </div>
</template>

<script>
export default {
  name: "ImportConfigTab",
  components: {},
  data() {
    return {  
    };
  },
  
  props: {
    model: Object,
    ansibleFacts: Object,
  }, 

  methods: {
    clearConfigData () {
      this.model.exportedConfigFolder = "";
      this.model.configPassword = "";
      this.model.validatorPassword = "";
      if (this.model.importValidator == true) {
        return this.model.importValidator = false;
      }
    },

    clearValidatorData () {
      this.model.validatorPassword = "";
    },
  },

  computed: {
    validateConfigFolder() {
      if (this.model.importConfig == true) {
          return (
            this.model.exportedConfigFolder.length > 0 && 
            this.model.exportedConfigFolder.startsWith("/") &&
            this.model.exportedConfigFolder.endsWith(".zip")
          );  
      } else { return null; }
    },

    validateConfigPassword() {
      if (this.model.importConfig == true) {
        return this.model.configPassword.length > 0
      } else { return null; }
    },

    validateValidatorPassword() {
      if (this.model.importValidator == true) {
        return this.model.validatorPassword.length > 0
      } else { return null; }
    },
  },
};
</script>

<style scoped></style>

