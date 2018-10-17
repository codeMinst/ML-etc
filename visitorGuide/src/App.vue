<template>
  <v-app>
    <v-toolbar dark class="purple darken-1" v-show="userIsAuthenticated" >
      <v-toolbar-side-icon @click.stop="sideNav = !sideNav"
      class="hidden-sm-and-up"></v-toolbar-side-icon>
      <v-toolbar-title><router-link to="/" tag="span" style="cursor: pointer">내방객안내시스템</router-link></v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-xs-only">
        <v-btn flat  v-for="item in menuItems" :key="item.title" :to="item.link" router>
          <v-icon left dark>{{item.icon}}</v-icon>
        {{item.title}}
        </v-btn>
        <v-btn flat v-if="userIsAuthenticated" @click="onLogout">
          <v-icon left dark>exit_to_app</v-icon></v-icon>
          Logout
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <main>
      <router-view></router-view>
			<video id="webCamWindow" autoplay style="display:none;"></video>
    </main>
  </v-app>
</template>

<script>
  export default {
    data () {
      return {
        sideNav: false
      }
    },
    computed: {
      menuItems () {
        let menuItems = [
          {icon: 'face', title: 'Sign up', link: '/signup'},
          {icon: 'lock_open', title: 'Sign in', link: '/user/signin'}
        ]
        if (this.userIsAuthenticated) {
          this.sideNav = true,
          menuItems = [
            {icon: 'supervisor_account', title: 'View Meetups', link: '/employees'}
          ]
        }
        return menuItems
      },
      userIsAuthenticated () {
        return this.$store.getters.user !== null && this.$store.getters.user !== undefined
      }
    },
    methods: {
      onLogout () {
        this.$store.dispatch('logout')
        this.$router.push('/')
      }
    }
  }
</script>
