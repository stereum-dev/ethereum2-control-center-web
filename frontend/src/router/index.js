import Vue from "vue";
import VueRouter from "vue-router";
import Setup from "../views/Setup.vue";
import ControlCenter from "../views/ControlCenter.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/", redirect: () => window.ENTRY },
  {
    path: "/setup",
    name: "setup",
    component: Setup,
  },
  {
    path: "/control-center",
    name: "control-center",
    component: ControlCenter,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
