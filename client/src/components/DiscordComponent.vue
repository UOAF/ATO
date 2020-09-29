<template>
<div v-if="user">
    <img :src="user.avatar_url" />
    <h2 class="text-center">Welcome to the ATO, {{ user.username }}</h2>
</div>
</template>

<script>
export default {
  name: "DiscordComponent",
  data() {
    return {
      user: null,
    };
  },
  created() {
    this.getUserData();
  },
  methods: {
    async getUserData() {
      fetch('/user/')
      .then(result => result.json())
      .then(data => this.user = data);
    }
  }
};
</script>
