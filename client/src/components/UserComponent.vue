<template>
  <div class="container-fluid">
    <b-navbar type="light" variant="light">
      <b-navbar-brand>ATO</b-navbar-brand>
      <template v-if="user">
        <b-navbar-nav class="ml-auto">
          <!-- Navbar dropdowns -->
          <b-nav-item-dropdown :text="user.username" right>
            <b-dropdown-item href="/logout/">Logout</b-dropdown-item>
          </b-nav-item-dropdown>

          <b-navbar-nav right>
            <img :src="user.avatar_url" height="40" />
          </b-navbar-nav>
        </b-navbar-nav>
      </template>
      <template v-else>
        <b-navbar-nav class="ml-auto" href="/login/">Login</b-navbar-nav>
      </template>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "UserComponent",
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
      fetch("/user/", { redirect: "error" })
        .then((result) => result.json())
        .then((data) => (this.user = data))
        .fail((err) => console.log("ERROR NOT LOGGED IN"));
    },
  },
};
</script>
