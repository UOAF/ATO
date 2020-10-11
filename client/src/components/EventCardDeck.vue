<template>
  <div>
    <b-card-group deck>
      <b-card
        v-for="e in events"
        :key="e.Event.Title"
        header="featured"
        header-tag="header"
        :title="e.Event.EventName"
      >
        <b-card-text>{{ e.Event.ShortDescription }}</b-card-text>
        <b-button href="#" variant="secondary" :to="`/event/${e.EventId}`"
          >View</b-button
        >
        <template v-slot:header>
          <small> {{ e.Event.StartTime | moment("llll") }}</small>
        </template>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
export default {
  name: "EventCardDeck",
  data() {
    return {
      events: null,
    };
  },
  created() {
    this.getEventData();
  },
  methods: {
    async getEventData() {
      fetch("/upcoming_events/4")
        .then((result) => result.json())
        .then((data) => (this.events = data.events));
    },
  },
};
</script>

