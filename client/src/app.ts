import "core-js/stable";
import "regenerator-runtime/runtime";
import Vue from 'vue';

// import HelloComponent from './components HelloComponent';
Vue.component('hello-component', require('./components/HelloComponent').default);

new Vue({
    el: '#app', 
    data: {
        message: 'Hello from Webpack'
    }
});

