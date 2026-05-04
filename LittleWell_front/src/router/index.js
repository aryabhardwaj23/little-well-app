import { createRouter, createWebHistory } from 'vue-router';

// Views
import HomePage from '../views/HomePage.vue';
import AboutPage from '../views/AboutPage.vue';
import QuickStartPage from '../views/QuickStartPage.vue';
import ChildInfoPage from '../views/ChildInfoPage.vue';
import NutritionNeedsPage from '../views/NutritionNeedsPage.vue';
import ProfileSummaryPage from '../views/ProfileSummaryPage.vue';
import NutritionCheckPage from '../views/NutritionCheckPage.vue';
import NutritionInsightsPage from '../views/NutritionInsightsPage.vue';
import ResultsPage from '../views/ResultsPage.vue';
import RecipePage from '../views/RecipePage.vue';
import WeeklyPlanPage from '../views/WeeklyPlanPage.vue';
import MyPlansPage from '../views/MyPlansPage.vue';

// Auth views
import LoginPage from '../views/LoginPage.vue';
import RegisterPage from '../views/RegisterPage.vue';

const routes = [
  // ── Auth routes ─────────────────────────────────────────────
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { title: 'Sign In - LittleWell', guestOnly: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
    meta: { title: 'Create Account - LittleWell', guestOnly: true },
  },

  // ── Public routes ───────────────────────────────────────────
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { title: 'Home - LittleWell' },
  },
  {
    path: '/about',
    name: 'About',
    component: AboutPage,
    meta: { title: 'About Us - LittleWell' },
  },
  {
    path: '/quick-start',
    name: 'QuickStart',
    component: QuickStartPage,
    meta: { title: 'Quick Start - LittleWell' },
  },
  {
    path: '/results',
    name: 'Results',
    component: ResultsPage,
    meta: { title: 'Lunchbox Results - LittleWell' },
  },
  {
    path: '/recipe/:id',
    name: 'Recipe',
    component: RecipePage,
    meta: { title: 'Recipe Details - LittleWell' },
  },

  // ── Protected app routes ────────────────────────────────────
  {
    path: '/nutrition-needs',
    name: 'NutritionNeeds',
    component: NutritionNeedsPage,
    meta: { title: 'Nutrition Needs - LittleWell', requiresAuth: true },
  },
  {
    path: '/child-info',
    name: 'ChildInfo',
    component: ChildInfoPage,
    meta: { title: 'Child Information - LittleWell', requiresAuth: true },
  },
  {
    path: '/profile-summary',
    name: 'ProfileSummary',
    component: ProfileSummaryPage,
    meta: { title: 'Profile Summary - LittleWell', requiresAuth: true },
  },
  {
    path: '/nutrition-check',
    name: 'NutritionCheck',
    component: NutritionCheckPage,
    meta: { title: 'Nutrition Check - LittleWell', requiresAuth: true },
  },
  {
    path: '/nutrition-insights',
    name: 'NutritionInsights',
    component: NutritionInsightsPage,
    meta: { title: 'Nutrition Insights - LittleWell', requiresAuth: true },
  },
  {
    path: '/weekly-plan',
    name: 'WeeklyPlan',
    component: WeeklyPlanPage,
    meta: { title: 'Weekly Plan - LittleWell', requiresAuth: true },
  },
  {
    path: '/my-plans',
    name: 'MyPlans',
    component: MyPlansPage,
    meta: { title: 'My Plans - LittleWell', requiresAuth: true },
  },

  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition;
    return { top: 0, behavior: 'smooth' };
  },
});

router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title || 'LittleWell - Seasonal Lunchbox Planning';

  const { useAuthStore } = await import('../stores/auth');
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({
      path: '/login',
      query: {
        redirect: to.fullPath,
      },
    });
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return next('/');
  }

  next();
});

export default router;