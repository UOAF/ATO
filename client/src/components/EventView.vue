<template>
  <b-container>
    <b-row fluid class="mt-4" align-v="start">
      <b-col fluid>
        <template v-if="event">
          <b-container fluid>
            <b-col>
              <b-row class="mb-0">
                <h1>{{ event.EventName }}</h1>
              </b-row>
              <b-row class="mb-3">
                <h5>{{ formatDate(event.StartTime) }}</h5>
              </b-row>
              <b-row class="mb-3">
                <h5>{{ event.ShortDescription }}</h5>
              </b-row>
              <b-row class="mb-2">
                <div v-html="compiledMarkdown"></div>
              </b-row>
            </b-col>
          </b-container>
        </template>
      </b-col>
      <b-col fluid>
        <b-row><b-img src="static/temp.png" fluid /> </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import marked from "marked";
import { DateTime } from "luxon";

export default {
  name: "EventView",
  data() {
    return {
      event: null,
    };
  },
  props: {
    user: Object,
  },
  computed: {
    compiledMarkdown() {
      if (this.event) {
        return marked(this.event.MissionDescription, { sanitize: true });
      } else {
        return "";
      }
    },
  },
  created() {
    this.updateEvent();
  },
  methods: {
    async updateEvent() {
      this.event_id = this.$route.params.id;
      fetch("/event/" + this.event_id, { redirect: "error" })
        .then((result) => result.json())
        .then((data) => (this.event = data))
        .catch((err) => console.log("ERROR getting event"));
    },
    formatDate(date_iso) {
      var dt = DateTime.fromISO(date_iso);
      return dt.toLocaleString(DateTime.DATETIME_FULL);
    },
  },
};
</script>
