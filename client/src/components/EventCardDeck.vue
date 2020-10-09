<template>
  <div>
    <b-card-group deck>
      <b-card
        v-for="event in events"
        :key="event.Title"
        header="featured"
        header-tag="header"
        :title="event.EventName"
      >
        <b-card-text>{{ event.MissionDescription }}</b-card-text>
        <b-button href="#" variant="secondary">Edit</b-button>
        <template v-slot:header>
          <small>{{ event.Date }} - {{ event.StartTime }}</small>
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
    this.getUserData();
  },
  methods: {
    async getUserData() {
      fetch("/getLatestEvents/")
        .then((result) => result.json())
        .then((data) => (this.events = data.events));
    },
  },
};
</script>

