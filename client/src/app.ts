import "core-js/stable";
import "regenerator-runtime/runtime";
import { DropdownPlugin, LayoutPlugin, NavbarPlugin } from "bootstrap-vue";
import Vue from "vue";

// Install BootstrapVue
Vue.use(LayoutPlugin);
Vue.use(DropdownPlugin);
Vue.use(NavbarPlugin);

// Optionally install the BootstrapVue icon components plugin (this adds ~6 seconds to webpack build)
// Vue.use(IconsPlugin)
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.component("AtoMain", require("./components/AtoMain").default);

new Vue({
  el: "#app",
  data: {
    message: "weirdo",
  },
});

var obj = {
  EventName: "Test Event 1",
  ShortDescription: "UPDATE EVENT TEST",
  MissionDescription: "We are testing shit. And mostly breaking shit.",
  Date: "2012-04-23",
  StartTime: "1800Z",
  EndTime: "2000Z",
  Creator: "Krause#5727",
  Controllers: [
    {
      Type: "ATC",
      Slots: [
        {
          SlotName: "Ramat David Tower",
          Players: [
            {
              "Player:": "Krause#5727",
              Remarks: "Gonna crash all you fuckers",
            },
          ],
        },
      ],
    },
  ],
  Packages: [
    {
      Commander: "Krause",
      Flights: [
        {
          FlightName: "Satan 1-1",
          Tasking: "DEAD",
          Airframe: "F-16CM Blk50",
          Airbase: "Ramat David",
          Slots: [
            {
              SlotName: "Satan 1-1",
              Players: [
                {
                  "Player:": "Krause#5727",
                  Type: "Pilot",
                  Remarks: "Sucks at agm-88",
                },
                {
                  "Player:": "R2D2#5727",
                  Type: "Backseat",
                  Remarks: "Weird f-16D that snuck in",
                },
              ],
            },
            {
              SlotName: "Satan 1-2",
              Players: [
                {
                  "Player:": "Abe#6969",
                  Remarks: "",
                },
              ],
            },
            {
              SlotName: "Satan 1-3",
              Players: [
                {
                  "Player:": "Razgriz#911",
                  Remarks: "Likes to smell butts",
                },
              ],
            },
            {
              SlotName: "Satan 1-4",
              Players: [
                {
                  "Player:": "Floppy#6969",
                  Remarks: "Yolo growler",
                },
              ],
            },
          ],
        },
      ],
    },
  ],
};
var json = JSON.stringify(obj);
// fetch('/updateEvent', {
// 	method: 'PUT',
// 	body: json, // The data
// 	headers: {
// 		'Content-type': 'application/json' // The type of data you're sending
// 	}
// });

/* fetch('/putEvent', {
	method: 'PUT',
	body: json, // The data
	headers: {
		'Content-type': 'application/json' // The type of data you're sending
	}
}); */
