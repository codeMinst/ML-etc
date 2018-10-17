import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import CreateEmployee from '@/components/employee/CreateEmployee'
import Employees from '@/components/employee/Employees'
import Signin from '@/components/user/Signin'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/employee/new',
      name: 'CreateEmployee',
      component: CreateEmployee
    },
    {
      path: '/employees',
      name: 'Employees',
      component: Employees
    },
    {
      path: '/user/signin',
      name: 'Signin',
      component: Signin
    }
  ],
  mode: 'history'
})
