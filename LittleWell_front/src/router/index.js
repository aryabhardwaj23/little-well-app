import { createRouter, createWebHistory } from 'vue-router';

// Views
import HomePage from '../views/HomePage.vue';
// import AboutPage from '../views/AboutPage.vue';
import QuickStartPage from '../views/QuickStartPage.vue';
import ChildProfilePage from '../views/ChildProfilePage.vue';
import ChildInfoPage from '../views/ChildInfoPage.vue';
// import NutritionNeedsPage from '../views/NutritionNeedsPage.vue';
// import ProfileSummaryPage from '../views/ProfileSummaryPage.vue';
// import NutritionCheckPage from '../views/NutritionCheckPage.vue';
// import NutritionInsightsPage from '../views/NutritionInsightsPage.vue';
import ResultsPage from '../views/ResultsPage.vue';
import RecipePage from '../views/RecipePage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { title: 'Home - LittleWell' }
  },
//   {
//     path: '/about',
//     name: 'About',
//     component: AboutPage,
//     meta: { title: 'About Us - LittleWell' }
//   },
  {
    path: '/quick-start',
    name: 'QuickStart',
    component: QuickStartPage,
    meta: { title: 'Quick Start - LittleWell' }
  },
//   {
//     path: '/nutrition-needs',
//     name: 'NutritionNeeds',
//     component: NutritionNeedsPage,
//     meta: { title: 'Nutrition Needs - LittleWell' }
//   },
  {
    path: '/child-profile',
    name: 'ChildProfile',
    component: ChildProfilePage,
    meta: { title: 'Child Profile - LittleWell' }
  },
  {
    path: '/child-info',
    name: 'ChildInfo',
    component: ChildInfoPage,
    meta: { title: 'Child Information - LittleWell' }
  },
//   {
//     path: '/profile-summary',
//     name: 'ProfileSummary',
//     component: ProfileSummaryPage,
//     meta: { title: 'Profile Summary - LittleWell' }
//   },
//   {
//     path: '/nutrition-check',
//     name: 'NutritionCheck',
//     component: NutritionCheckPage,
//     meta: { title: 'Nutrition Check - LittleWell' }
//   },
//   {
//     path: '/nutrition-insights',
//     name: 'NutritionInsights',
//     component: NutritionInsightsPage,
//     meta: { title: 'Nutrition Insights - LittleWell' }
//   },
  {
    path: '/results',
    name: 'Results',
    component: ResultsPage,
    meta: { title: 'Lunchbox Results - LittleWell' }
  },
  {
    path: '/recipe/:id',
    name: 'Recipe',
    component: RecipePage,
    meta: { title: 'Recipe Details - LittleWell' }
  },
//   {
//     path: '/:pathMatch(.*)*',
//     redirect: '/',
//   },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0, behavior: 'smooth' };
    }
  },
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'LittleWell - Seasonal Lunchbox Planning';
  next();
});

export default router;
