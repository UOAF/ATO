import Vue from 'vue';
Vue.component('hello-component', require('./components/HelloComponent').default);

new Vue({
    el: '#app', 
    data: {
        message: 'Hello from Webpack'
    }
});

