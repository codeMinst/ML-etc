// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import * as firebase from 'firebase'
import router from './router'
import { store } from './store'
import Vuetify from 'vuetify'
import axios from 'axios'
import blob from 'blob'
import 'vuetify/dist/vuetify.min.css'
import DetailInfoDialog from './components/employee/DetailInfoDialog.vue'
import EditEmployeeDialog from './components/employee/EditEmployeeDialog.vue'
import CommuteLogDialog from './components/employee/CommuteLogDialog.vue'
import InoutLogDialog from './components/employee/InoutLogDialog.vue'

Vue.use(Vuetify)
Vue.config.productionTip = false
Vue.prototype.$http = axios

Vue.component('detail-info-dialog', DetailInfoDialog)
Vue.component('edit-employee-dialog', EditEmployeeDialog)
Vue.component('commute-log-dialog', CommuteLogDialog)
Vue.component('inout-log-dialog', InoutLogDialog)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App),
  created () {
    firebase.initializeApp ({
      apiKey: "AIzaSyAq65CtCXPzYeluWt93zb498tvSQh8nkUo",
      authDomain: "vue-visitor-guide.firebaseapp.com",
      databaseURL: "https://vue-visitor-guide.firebaseio.com",
      projectId: "vue-visitor-guide",
      storageBucket: "vue-visitor-guide.appspot.com"
    })
    firebase.auth().onAuthStateChanged((user) => {
      if(user) {
        this.$store.dispatch('autoSignIn', user)
        this.$store.dispatch('fetchUserData', user)
      }
    })
    this.$store.dispatch('loadEmployees')
    this.$store.dispatch('sipStart')
  }
})
