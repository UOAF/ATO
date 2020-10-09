<template>
  <b-container>
    <b-row fluid>
      <b-col>
        <user-component v-if="user" v-bind:user="user" />
      </b-col>
    </b-row>
    <b-row fluid class="mt-4" align-v="end">
      <b-col fluid>
        <event-card-deck />
      </b-col>
      <b-col cols="12" md="auto">
        <b-button variant="primary"> New </b-button>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import UserComponent from "./UserComponent.vue";
import EventCardDeck from "./EventCardDeck.vue";
export default {
  components: {
    "user-component": UserComponent,
    "event-card-deck": EventCardDeck,
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
