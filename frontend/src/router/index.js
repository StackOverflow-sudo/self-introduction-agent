import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Chat from '../views/Chat.vue'
import Projects from '../views/Projects.vue'
import About from '../views/About.vue'
import NotFound from '../views/NotFound.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/chat', name: 'chat', component: Chat },
  { path: '/projects', name: 'projects', component: Projects },
  { path: '/about', name: 'about', component: About },
  { path: '/preview', name: 'preview', component: () => import('../views/ModelPreview.vue') },
  { path: '/:pathMatch(.*)*', name: 'notfound', component: NotFound },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})