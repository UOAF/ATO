<template>
  <b-navbar type="light" variant="light">
    <b-navbar-brand>UOAF Event Schedule</b-navbar-brand>
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
</template>

<script>
export default {
  name: "UserComponent",

  props: {
    user: Object,
  },
};
</script>
