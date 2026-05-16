import { createRouter, createWebHistory } from 'vue-router';

import HomePage from '../views/HomePage.vue';
import QuickStartPage from '../views/QuickStartPage.vue';
import ChildProfilePage from '../views/ChildProfilePage.vue';
import ChildInfoPage from '../views/ChildInfoPage.vue';
import ResultsPage from '../views/ResultsPage.vue';
import RecipePage from '../views/RecipePage.vue';
import FoodAnalyserPage from '../views/FoodAnalyserPage.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage, meta: { title: 'Home - LittleWell' } },
  { path: '/quick-start', name: 'QuickStart', component: QuickStartPage, meta: { title: 'Quick Start - LittleWell' } },
  { path: '/child-profile', name: 'ChildProfile', component: ChildProfilePage, meta: { title: 'Child Profile - LittleWell' } },
  { path: '/child-info', name: 'ChildInfo', component: ChildInfoPage, meta: { title: 'Child Information - LittleWell' } },
  { path: '/results', name: 'Results', component: ResultsPage, meta: { title: 'Lunchbox Results - LittleWell' } },
  { path: '/recipe/:id', name: 'Recipe', component: RecipePage, meta: { title: 'Recipe Details - LittleWell' } },
  { path: '/food-analyser', name: 'FoodAnalyser', component: FoodAnalyserPage, meta: { title: 'Food Analyser - LittleWell' } },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0, behavior: 'smooth' };
  },
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'LittleWell - Seasonal Lunchbox Planning';
  next();
});

export default router;
