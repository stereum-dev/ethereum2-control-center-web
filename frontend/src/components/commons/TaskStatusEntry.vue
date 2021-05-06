<template>
  <li>
    <span
      class="dot"
      :class="model.status == 0 ? 'dot-success' : 'dot-danger'"
    ></span>
    <span class="taskname">{{ model.name }}</span>
    <span v-if="model.status > 0" class="taskerror">
      <data>{{ model }}</data>
    </span>
  </li>
</template>

<script>
export default {
  name: "TaskStatusEntry",
  components: {},
  props: {
    model: Object,
  },
};
</script>

<style scoped>
.taskname {
  margin-left: 10px;
}
.dot {
  display: inline-block;
  border-radius: 50%;
  width: 50%;
  background-color: #eee;
  height: 15px;
  width: 15px;
  margin: 0 2px;
}
.dot.dot-success {
  background-color: #449d44;
}
.dot.dot-warning {
  background-color: #f0ad4e;
}
.dot.dot-danger {
  background-color: #d9534f;
}
.dot.dot-sm {
  height: 10px;
  width: 10px;
}
.dot.dot-lg {
  margin: 0 4px;
  height: 20px;
  width: 20px;
}
</style>
