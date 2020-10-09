<template>
  <user-component v-if="user" />
</template>

<script>
import UserComponent from "./UserComponent.vue";
export default {
  components: {
    "user-component": UserComponent,
  },
  name: "AtoMain",
  data() {
    return {
      user: null,
    };
  },
  created() {
    this.getUserData();
  },
  methods: {
    async getUserData() {
      fetch("/user/")
        .then((result) => result.json())
        .then((data) => (this.user = data));
    },
  },
};
</script>
