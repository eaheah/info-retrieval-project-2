import Vue from 'vue'
import Router from 'vue-router'
// import Home from '@/components/Home'
import Results from '@/components/Results'

Vue.use(Router)

export default new Router({
  scrollBehaviour() {
    return { x: 0, y: 0 }
  },
  routes: [
    // {
    //   path: '/',
    //   name: 'Home',
    //   component: Home
    // },
    {
      path: '/search/:searchID',
      name: 'search',
      component: Results
    }
  ]
})