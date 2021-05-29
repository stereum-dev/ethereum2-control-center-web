<template>
  <li @click="showDetails">    
    <i :class="model.status == 0 ? 'fas success fa-check ' : 'fa danger fa-exclamation-triangle'"></i>
    <span class="taskname">{{ model.name || 'Unnamed Task' }}</span>
    <span v-if="model.status > 0" class="taskerror">
      <span>: {{ model.message.msg }} (click for details)</span>            
    </span>
    <div v-if="details">
      <data>{{ model.message }}</data>
    </div>
  </li>
</template>

<script>
export default {
  name: "TaskStatusEntry",
  components: {},
  props: {
    model: Object,
  },
  data() {
    return {
      details: false,
    };
  },
  methods: {
    showDetails() {
      this.details = !this.details;
    }
  }
};
</script>

<style scoped>

 .list-group-item {
   padding: 1px;
   border: 0px;
 }

 .success {
   color: #28a745;
 }

 .danger {
   color: #dc3545;
 }

.taskname {
  margin-left: 10px;
}
</style>
