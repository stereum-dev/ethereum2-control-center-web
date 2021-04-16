<template>
  <div>
    <b-card            
      img-src="https://picsum.photos/600/50/?grayscale"
      img-alt="Image"
      img-top
      tag="article"
      style="max-width: 20rem;"
      class="mb-2 main-card"      
    >
      <b-card-body>
        <div>
          <form-wizard          
            shape="square"
            color="#336666"
            title='Guided Beacon Installer'
            subtitle='Setup your Beacon'
            finishButtonText='Start Installation'
            @on-complete="onComplete"
            :hide-buttons="installationRunning"
          >          
            <tab-content title="Welcome" icon="faw fas fa-door-open">                        
              <welcome-tab></welcome-tab>            
            </tab-content>
            <tab-content title="Network" icon="faw fas fa-network-wired">
              <network-tab :model="model"></network-tab>
            </tab-content>
            <tab-content title="Client" icon="faw fas fa-cogs">
              <client-tab :model="model"></client-tab>
            </tab-content>
            <tab-content title="Path" icon="faw far fa-folder-open" :before-change="()=>validateInstallationFolder()">
              <installation-folder-tab :model="model"></installation-folder-tab>
            </tab-content>          
            <tab-content title="Verify" icon="faw fas fa-check-double">
              <verification-tab :model="model" :progress="installationProgress" :running="installationRunning"></verification-tab>
            </tab-content>          
          </form-wizard>
        </div>        
      </b-card-body>      
    </b-card>
  </div>
</template>

<script>
//local registration
import {FormWizard, TabContent} from 'vue-form-wizard'
import 'vue-form-wizard/dist/vue-form-wizard.min.css'
import '@fortawesome/fontawesome-free/css/all.css'
import WelcomeTab from '@/components/wizard/WelcomeTab.vue'
import NetworkTab from '@/components/wizard/NetworkTab.vue'
import ClientTab from '@/components/wizard/ClientTab.vue'
import InstallationFolderTab from '@/components/wizard/InstallationFolderTab.vue'
import VerificationTab from '@/components/wizard/VerificationTab.vue'

export default {
  name: "SetupWizard",
  components: {
    FormWizard,
    TabContent,
    WelcomeTab,
    NetworkTab,
    ClientTab,
    InstallationFolderTab,
    VerificationTab,    
  },
  data () {
    return {     
      installationRunning: false, 
      installationProgress: 0,
    }
  },
  props: {    
    model: Object
  },
  methods: {
    validateInstallationFolder() {      
      return this.model.installationFolder && this.model.installationFolder.startsWith('/');
    },    
    onComplete: function() {      
      this.installationRunning = true;      
      this.installationProgress=0;
      
      let handle = null;
      const f = () => {
        this.installationProgress+=1;        
        if (this.installationProgress == 100) {          
          clearInterval(handle);
          this.installationRunning = false;      
          this.installationProgress= 0;
        }
      };
      handle = setInterval(f, 500)
    },    
  },  
};
</script>

<style scoped>
  .main-card {
    margin-top: 5%;
    margin-left: 10%;
    margin-right: 10%;
    min-width: 80%;
  }

  .main-card img {
    max-height: 50px;
  }
</style>
