<template>
  <b-container>
    <b-row fluid class="mt-4" align-v="start">
      <b-col fluid>
        <template v-if="event">
          <b-container>
            <b-row fluid>
              <b-col
                ><h3>{{ event.EventName }}</h3></b-col
              >
            </b-row>
            <b-row fluid>
              <b-col>
                <h5>{{ event.ShortDescription }}</h5>
              </b-col>
            </b-row>
            <b-row fluid>
              <b-col><div v-html="compiledMarkdown"></div></b-col>
            </b-row>
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
  },
};
</script>
