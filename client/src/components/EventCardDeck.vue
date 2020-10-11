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
          <small>
            {{ formattedDate(e.Event.StartTime) }}
          </small>
        </template>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import {DateTime} from "luxon";
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
  computed: {},
  methods: {
    async getEventData() {
      fetch("/upcoming_events/4")
        .then((result) => result.json())
        .then((data) => (this.events = data.events));
    },
    formattedDate(date_iso) {
      if (!date_iso) {
        return "";
      }
      var dt = DateTime.fromISO(date_iso);
      return dt.toLocaleString(DateTime.DATETIME_FULL);
    },
  },
};
</script>

