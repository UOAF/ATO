<template>
  <b-container>
    <b-row fluid align-v="start">
      <b-col fluid>
        <event-card-deck />
      </b-col>
      <b-col cols="12" md="auto" v-if="user && user.admin">
        <b-button variant="primary"> New </b-button>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import EventCardDeck from "./EventCardDeck.vue";
export default {
  name: "EventCalendar",
  props: {
    user: Object,
  },
  components: {
    "event-card-deck": EventCardDeck,
  },
};
</script>
