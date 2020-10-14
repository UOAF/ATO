import "core-js/stable";
import "regenerator-runtime/runtime";
import {
  ButtonPlugin,
  CardPlugin,
  DropdownPlugin,
  LayoutPlugin,
  NavbarPlugin,
  ImagePlugin,
  BIcon,
  BIconPlus,
  BIconArrow90degLeft
} from "bootstrap-vue";
import VueRouter from "vue-router";
import Vue from "vue";

// Install BootstrapVue
Vue.use(LayoutPlugin);
Vue.use(DropdownPlugin);
Vue.use(NavbarPlugin);
Vue.use(CardPlugin);
Vue.use(ButtonPlugin);
Vue.use(VueRouter);
Vue.use(ImagePlugin);
Vue.component('BIcon', BIcon);
Vue.component('BIconPlus', BIconPlus);
Vue.component('BIconArrow90degLeft', BIconArrow90degLeft);

// Optionally install the BootstrapVue icon components plugin (this adds ~6 seconds to webpack build)
// Vue.use(IconsPlugin)
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import AtoMain from "./components/AtoMain.vue";
import EventCalendar from "./components/EventCalendar.vue";
import EventView from "./components/EventView.vue";

const routes = [
  {
    path: "/",
    component: AtoMain,
    children: [
      { path: "", component: EventCalendar },
      { path: "/event/:id", component: EventView },
    ],
  },
];

const router = new VueRouter({
  routes, // short for `routes: routes`
});

new Vue({
  router,
  el: "#app",
}).$mount("#app");

var obj = {
  EventName: "Test Event 1",
  ShortDescription: "UPDATE EVENT TEST",
  MissionDescription: "We are testing shit. And mostly breaking shit.",
  StartTime: "2012-10-09T18:00:00.000Z",
  EndTime: "2012-10-09T22:00:00.000Z",
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
});
 */
