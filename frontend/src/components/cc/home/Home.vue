<template>
  <div class="wrapper">
    <div class="homepage"></div>
  </div>
</template>

<script>
export default {
  name: "Home",
  components: {},
  data() {
    return {};
  },
  props: {
    model: Object,
  },
};
</script>

<style scoped>
.wrapper{
   position: absolute;
   padding-top: 50px;
   padding-bottom: 20px;
   width: 100%;
   height: 94%;
   text-align: center;
}
.homepage{
   margin: auto;
   width: 90%;
   height: 95%;
   background: url('/public/homepage.png');
   background-size: contain;
   background-repeat: no-repeat;
   background-position: center center;
}
</style>
