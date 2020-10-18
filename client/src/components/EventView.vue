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
                      :src="getUserData(pkg.CommanderId).avatar_url"
                      size="1.5em"
                    ></b-avatar>
                    {{ getUserData(pkg.CommanderId).username }}
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
                      <th>Role</th>
                      <th>Player</th>
                      <th>Remarks</th>
                    </tr>
                    <tr v-for="slot in flight.Slots" :key="slot.SlotName">
                      <td class="bg-light editable">{{ slot.SlotName }}</td>
                      <td class="bg-light editable">{{ slot.Type }}</td>
                      <td class="bg-light editable" v-if="slot.PlayerId">
                        <b-avatar
                          :src="getUserData(slot.PlayerId).avatar_url"
                          size="1.5em"
                        ></b-avatar>
                        {{ getUserData(slot.PlayerId).username }}
                      </td>
                      <td v-else></td>
                      <td class="bg-light editable">
                        {{ slot.Remarks }}
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
      userIds: [],
      userMap: {},
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
    async fetchUserInfo(userId) {
      let resp = await fetch("/user/".concat(userId));
      if (!resp.ok) {
        console.error("Http error ${resp.status} getting user ${userId}.");
      }
      return await resp.json();
    },

    getUserData(userId) {
      const userObj =
        userId in this.userMap
          ? this.userMap[userId]
          : { username: "", avatar_url: "" };
      return userObj;
    },

    async updateEvent() {
      const eventId = this.$route.params.id;
      let self = this;
      try {
        let resp = await fetch("/event/" + eventId, {
          redirect: "error",
        });
        let data = await resp.json();

        ////////////////////////////////////////////////////////////
        // Iterate through the event data. Returns an array of all
        // user ids found in the event.
        ////////////////////////////////////////////////////////////
        const findAllUsersInEvent = function () {
          let userIds = [];

          const addUserId = function (userId) {
            const notAlreadyStored = !userIds.includes(userId);
            const notEmpty = userId != "";
            if (notEmpty && notAlreadyStored) {
              userIds.push(userId);
            }
          };
          for (const controller of data.Controllers) {
            for (const slot of controller.Slots) {
              for (const player of slot.Players) {
                addUserId(player.PlayerId);
              }
            }
          }
          for (const pkg of data.Packages) {
            userIds.push(pkg.CommanderId);
            for (const flight of pkg.Flights) {
              for (const slot of flight.Slots) {
                for (const player of slot.Players) {
                  addUserId(player.PlayerId);
                }
              }
            }
          }
          return userIds;
        };

        ////////////////////////////////////////////////////////////
        // Fetch all relevant user info data in parallel using
        // async io
        ////////////////////////////////////////////////////////////
        const makeUserMap = async function (userIds) {
          const users = await Promise.all(
            userIds.map((uid) => self.fetchUserInfo(uid))
          );

          return Object.fromEntries(
            self.userIds.map((uid, idx) => [uid, users[idx]])
          );
        };

        ////////////////////////////////////////////////////////////
        // Rearrange the slot structure to contain player info for
        // each slot. This makes rendering the signup table much
        // easier.
        ////////////////////////////////////////////////////////////
        const flattenSlots = function (slots) {
          let new_slots = [];
          for (let slot of slots) {
            const players = slot.Players;
            delete slot.Players;
            let idx = 0;
            for (let player of players) {
              const role = player.Type ? player.Type : "Pilot";
              const slot_name = 0 == idx ? slot.SlotName : "";
              new_slots.push({
                PlayerId: player.PlayerId,
                SlotName: slot_name,
                Type: role,
                Remarks: player.Remarks,
              });
              idx++;
            }
          }
          return new_slots;
        };

        this.userIds = findAllUsersInEvent(data);

        for (let pkg of data.Packages) {
          for (let flight of pkg.Flights) {
            flight.Slots = flattenSlots(flight.Slots);
          }
        }

        this.event = data;
        this.userMap = await makeUserMap(this.userIds);
      } catch (err) {
        console.log(err);
        console.log("ERROR getting event");
      }
    },
    formatDate(date_iso) {
      const dt = DateTime.fromISO(date_iso);
      return dt.toLocaleString(DateTime.DATETIME_FULL);
    },
  },
};
</script>
