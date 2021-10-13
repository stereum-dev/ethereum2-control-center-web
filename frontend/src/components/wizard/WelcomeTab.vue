<template>
  <div class="text-left">
    <h3>Welcome</h3>
    In the following steps we will guide you through setting up your own Ethereum Node. If you should run into any problems or need assistance with the setup, join our <b-link href="https://discord.gg/8Znj8K6GjN">Discord</b-link> - we are happy to help you out.

    <b-alert 
      v-if="ansibleFacts !== undefined && (ansibleFacts.distribution === 'Ubuntu' || ansibleFacts.distribution === 'CentOS')"
      show
      variant="success"
      class="mt-3"
      >Your OS looks good, we support Ubuntu and CentOS.
    </b-alert>
    <b-alert 
      v-else-if="ansibleFacts !== undefined"
      show
      variant="danger"
      class="mt-3"
      >Your OS {{ ansibleFacts.distribution }} is not supported! Please use either Ubuntu or Centos!
    </b-alert>
    <b-alert 
      v-else
      show
      variant="primary"
      class="mt-3"
      >Checking if the OS of your server is supported...&nbsp;<i class="fas fa-cog fa-spin"></i>
    </b-alert>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "WelcomeTab",
  components: {},
  data() {
    return {
      processStatus: {
        response: "",
        logs: {
          tasks: [],
        },
        running: false,
        done: false,
        progress: 0,
        success: undefined,
      },
      ansibleFacts: undefined,
    };
  },
  props: {
    model: Object,
    setAnsibleFacts: Function,
  },
  created() {
    this.pullHardwareSpecs();
  },
  methods: {
    pullHardwareSpecs() {
      this.readData("read-ansible-facts", {}, this.refreshSpecsModel);
    },

    refreshSpecsModel: function() {
      this.ansibleFacts = this.processStatus.logs.tasks[1].message.ansible_facts;
      
      console.log("OS: " + this.ansibleFacts.distribution);
      console.log("CPUs: " + this.ansibleFacts.processor_vcpus);
      console.log("Memory: " + this.ansibleFacts.memtotal_mb);
      console.log(this.ansibleFacts.mounts);

      this.setAnsibleFacts(this.ansibleFacts);
    },

    readData: function(control, data, ...callbacks) {
      if (this.processStatus.running === false) {
        this.processStatus.running = true;
        this.processStatus.progress = 0;
        this.processStatus.done = false;
        this.processStatus.success = undefined;
        this.processStatus.logs = { tasks: [], };

        const payload = {
          inventory: "inventory.yaml",
          playbook: control,
          extra_vars: data,
          extraVars: data,
        };

        const fetchStatus = () => {
          axios.get("/api/setup/status", {"apikey": window.APIKEY}).then((response) => {
            //console.log(response.data);
            this.processStatus.logs = response.data;
            this.processStatus.progress = response.data.tasks.length;
            callbacks.forEach(cb => cb.apply());
          });
        };

        axios
          .post("/api/setup/start", payload, {"apikey": window.APIKEY})
          .then((response) => {
            if (response.data.status > 0) {
              this.$toasted.error(
                "Can't read hardware specs!",
                { duration: 5000 }
              );
              this.processStatus.progress = 0;
              this.processStatus.success = false;
            }
            if (response.data.status <= 0) {
              this.processStatus.progress = 100;
              this.processStatus.success = true;
            }
            this.processStatus.running = false;
            this.processStatus.done = true;
            fetchStatus(); // do a final status fetch
          })
          .catch((error) => {
            if (error.message == 'data read: Request failed with status code 404') {
              this.$toasted.error(
                "data read: Backend not reachable (http return code 404).",
                { duration: 5000 }
              );
            } else {
              this.$toasted.error(
                "data read:Unfortunately an error has occured during the changes",
                { duration: 5000 }
              );
            }
            console.error(error);
            this.processStatus.progress = 0;
            this.processStatus.running = false;
            this.processStatus.done = true;
          });
      }
    },
  }
};
</script>
