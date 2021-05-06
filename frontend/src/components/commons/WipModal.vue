<template>
  <b-modal
    id="workinprogress-modal"
    size="lg"
    scrollable
    centered
    title="Work in Progress"
    no-close-on-backdrop
  >
    <b-progress
      v-if="running"
      :value="progress"
      variant="info"
      :max="max"
      show-progress
      animated
    >
      <b-progress-bar :value="progress">
        <span
          >Progress: <strong>{{ progress.toFixed(0) }}%</strong></span
        >
      </b-progress-bar>
    </b-progress>
    <strong class="text-left">Logs:</strong>
    <ul class="list-group list-unstyled">
      <task-status-entry
        class="list-group-item text-left"
        v-bind:key="index"
        v-for="(status, index) in logs"
        :model="status"
      ></task-status-entry>
    </ul>
  </b-modal>
</template>

<script>
import TaskStatusEntry from "@/components/commons/TaskStatusEntry.vue";

export default {
  name: "WorkInProgressModal",
  components: {
    TaskStatusEntry,
  },
  props: {
    model: Object,
    running: Boolean,
    done: Boolean,
    progress: Number,
    logs: Array,
  },
  data() {
    return {
      max: 100,
    };
  },
  mounted() {},
  methods: {},
};
</script>

<style scoped></style>
