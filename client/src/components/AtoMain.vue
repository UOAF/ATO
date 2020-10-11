<template>
  <b-container>
    <b-row fluid>
      <b-col>
        <user-component v-if="user" v-bind:user="user" />
      </b-col>
    </b-row>
    <b-row fluid class="mt-4">
      <b-col>
        <router-view v-bind:user="user"></router-view>
      </b-col>
    </b-row>
  </b-container>
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
      fetch("/user/", { redirect: "error" })
        .then((result) => result.json())
        .then((data) => (this.user = data))
        .catch((err) => console.log("ERROR NOT LOGGED IN"));
    },
  },
};
</script>
