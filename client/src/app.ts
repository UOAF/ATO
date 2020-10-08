import "core-js/stable";
import "regenerator-runtime/runtime";
import Vue from 'vue';


// const data = { username: 'example' };

// fetch('https://example.com/profile', {
//   method: 'PUT', // or 'POST'
//   headers: {
//     'Content-Type': 'application/json',
//   },
//   body: JSON.stringify(data),
// })
// .then(response => response.json())
// .then(data => {
//   console.log('Success:', data);
// })
// .catch((error) => {
//   console.error('Error:', error);
// });


// import HelloComponent from './components HelloComponent';
Vue.component('hello-component', require('./components/HelloComponent').default);

new Vue({
    el: '#app', 
    data: {
        message: 'Hello from Webpack'
    }
});

var obj = 
(
    {
        "EventName": "Test Event 1",
        "ShortDescription": "UPDATE EVENT TEST",
        "MissionDescription": "We are testing shit. And mostly breaking shit.",
        "Date": "2012-04-23",
        "StartTime": "1800Z",
        "EndTime": "2000Z",
        "Creator": "Krause#5727",
        "Controllers": [
            {
                "Type": "ATC",
                "Slots": [
                    {
                        "SlotName": "Ramat David Tower",
                        "Players": [
                            {
                                "Player:": "Krause#5727",
                                "Remarks": "Gonna crash all you fuckers"
                            }
                        ]
                    }
                ]
            }
        ],
        "Packages": [
            {
                "Commander": "Krause",
                "Flights": [
                    {
                        "FlightName": "Satan 1-1",
                        "Tasking": "DEAD",
                        "Airframe": "F-16CM Blk50",
                        "Airbase": "Ramat David",
                        "Slots": [
                            {
                                "SlotName": "Satan 1-1",
                                "Players": [
                                    {
                                        "Player:": "Krause#5727",
                                        "Type": "Pilot",
                                        "Remarks": "Sucks at agm-88"
                                    },
                                    {
                                        "Player:": "R2D2#5727",
                                        "Type": "Backseat",
                                        "Remarks": "Weird f-16D that snuck in"
                                    }
                                ]
                            },
                            {
                                "SlotName": "Satan 1-2",
                                "Players": [
                                    {
                                        "Player:": "Abe#6969",
                                        "Remarks": ""
                                    }
                                ]
                            },
                            {
                                "SlotName": "Satan 1-3",
                                "Players": [
                                    {
                                        "Player:": "Razgriz#911",
                                        "Remarks": "Likes to smell butts"
                                    }
                                ]
                            },
                            {
                                "SlotName": "Satan 1-4",
                                "Players": [
                                    {
                                        "Player:": "Floppy#6969",
                                        "Remarks": "Yolo growler"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
);
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