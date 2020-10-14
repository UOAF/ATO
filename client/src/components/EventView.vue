<template>
  <b-container>
    <b-row class="mt-4" align-v="start">
      <b-col>
        <template v-if="event">
          <b-container>
            <b-col>
              <b-row class="mb-0">
                <b-col>
                  <h1>{{ event.EventName }}</h1>
                </b-col>
              </b-row>
              <b-row class="mb-3">
                <b-col>
                  <h5>{{ formatDate(event.StartTime) }}</h5>
                </b-col>
              </b-row>
              <b-row class="mb-3">
                <b-col>
                  <h5>{{ event.ShortDescription }}</h5>
                </b-col>
              </b-row>
              <b-row class="mb-2">
                <b-col>
                  <div v-html="compiledMarkdown"></div>
                </b-col>
              </b-row>
            </b-col>
          </b-container>
        </template>
      </b-col>
      <b-col cols="7">
        <b-row>
          <b-col>
            <h5>Flights</h5>
          </b-col>
        </b-row>
        <template v-if="event">
          <b-row
            v-for="pkg in event.Packages"
            :key="pkg.Identifier"
            align-v="center"
          >
            <div style="width: 100%">
              <table class="pkgform">
                <tr>
                  <td>
                    <b-button
                      variant="light"
                      size="xs"
                      v-b-toggle.collapse-pkg
                      class="btn-xs"
                    >
                      <b-icon
                        icon="arrow-90deg-left"
                        scale="0.7"
                        rotate="180"
                        aria-hidden="true"
                      >
                      </b-icon>
                    </b-button>
                  </td>
                  <td><b>Package</b></td>
                  <td class="bg-light editable">{{ pkg.Identifier }}</td>
                  <td><b>Commander:</b></td>
                  <td class="bg-light editable">
                    <b-avatar
                      :src="pkg.Commander.avatar_url"
                      size="1.5em"
                    ></b-avatar>
                    {{ pkg.Commander.username }}
                  </td>
                </tr>
              </table>
            </div>
            <div
              style="margin-left: 1em"
              v-for="flight in pkg.Flights"
              :key="flight.FlightName"
            >
              <b-collapse visible id="collapse-pkg">
                <table class="pkgform">
                  <tr>
                    <th></th>
                    <th>Flight</th>
                    <th>Tasking</th>
                    <th>Airframe</th>
                    <th>Base</th>
                  </tr>
                  <tr>
                    <td>
                      <b-button
                        variant="light"
                        size="xs"
                        v-b-toggle.collapse-flight
                        class="btn-xs"
                      >
                        <b-icon
                          icon="arrow-90deg-left"
                          scale="0.7"
                          rotate="180"
                          aria-hidden="true"
                        >
                        </b-icon>
                      </b-button>
                    </td>
                    <td class="bg-light editable">{{ flight.FlightName }}</td>
                    <td class="bg-light editable">{{ flight.Tasking }}</td>
                    <td class="bg-light editable">{{ flight.Airframe }}</td>
                    <td v-if="flight.Airbase" class="bg-light editable">
                      {{ flight.Airbase }}
                    </td>
                  </tr>
                </table>
                <b-collapse visible id="collapse-flight">
                  <table class="pkgform" style="width: 100%; margin-left: 2em">
                    <tr>
                      <th>Slot</th>
                      <th>Player</th>
                      <th>Remarks</th>
                    </tr>
                    <tr v-for="slot in flight.Slots" :key="slot.SlotName">
                      <td class="bg-light editable">{{ slot.SlotName }}</td>
                      <td class="bg-light editable" v-if="slot.Players[0].User">
                        <b-avatar
                          :src="slot.Players[0].User.avatar_url"
                          size="1.5em"
                        ></b-avatar>
                        {{ slot.Players[0].User.username }}
                      </td>
                      <td class="bg-light editable">
                        {{ slot.Players[0].Remarks }}
                      </td>
                    </tr>
                  </table>
                </b-collapse>
              </b-collapse>
            </div>
          </b-row>
        </template>
        <!-- <b-row><b-img src="static/temp.png" /> </b-row> -->
      </b-col>
    </b-row>
  </b-container>
</template>

<style>
.btn-xs {
  padding-left: 0 !important;
  padding-right: 0 !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  font-size: 0.5em;
}

td.editable {
  padding-left: 0.6em;
  padding-right: 0.6em;
  /* background-color: rgb(235, 235, 235); */
  border-radius: 0.3em;
}

table.pkgform {
  border-spacing: 8px 4px;
  border-collapse: unset;
}

td.indent {
  padding-left: 0.8em;
}
</style>

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
    async getUserInfo(user_id) {
      let resp = await fetch("/user/".concat(user_id));
      if (!resp.ok) {
        console.error("Http error ${resp.status} getting user ${user_id}.");
      }
      return await resp.json();
    },

    async updateEvent() {
      this.event_id = this.$route.params.id;
      try {
        let resp = await fetch("/event/" + this.event_id, {
          redirect: "error",
        });
        let data = await resp.json();

        await Promise.all(
          data.Packages.map(async (p) => {
            p.Commander = await this.getUserInfo(p.CommanderId);
            return Promise.all(
              p.Flights.map(async (flight) =>
                Promise.all(
                  flight.Slots.map(async (slot) =>
                    Promise.all(
                      slot.Players.map(async (player) => {
                        let info = await this.getUserInfo(player.PlayerId);
                        player.User = info;
                        return player;
                      })
                    )
                  )
                )
              )
            );
          })
        );
        this.event = data;
      } catch (err) {
        console.log(err);
        console.log("ERROR getting event");
      }
    },
    formatDate(date_iso) {
      var dt = DateTime.fromISO(date_iso);
      return dt.toLocaleString(DateTime.DATETIME_FULL);
    },
  },
};
</script>
