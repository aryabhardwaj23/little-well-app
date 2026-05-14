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
import KnowledgeHubPrototype from '../views/KnowledgeHubPrototype.vue';

// Auth views
import LoginPage from '../views/LoginPage.vue';
import RegisterPage from '../views/RegisterPage.vue';

// Project access view
import ProjectAccessPage from '../views/ProjectAccessPage.vue';

const routes = [
  {
    path: '/project-access',
    name: 'ProjectAccess',
    component: ProjectAccessPage,
    meta: {
      title: 'Project Access - LittleHelp',
      skipProjectAccess: true,
    },
  },

  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { title: 'Sign In - LittleHelp', guestOnly: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
    meta: { title: 'Create Account - LittleHelp', guestOnly: true },
  },

  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { title: 'Home - LittleHelp' },
  },
  {
    path: '/about',
    name: 'About',
    component: AboutPage,
    meta: { title: 'About Us - LittleHelp' },
  },
  {
    path: '/quick-start',
    name: 'QuickStart',
    component: QuickStartPage,
    meta: { title: 'Quick Start - LittleHelp' },
  },
  {
    path: '/results',
    name: 'Results',
    component: ResultsPage,
    meta: { title: 'Lunchbox Results - LittleHelp' },
  },
  {
    path: '/recipe/:id',
    name: 'Recipe',
    component: RecipePage,
    meta: { title: 'Recipe Details - LittleHelp' },
  },

  {
    path: '/nutrition-needs',
    name: 'NutritionNeeds',
    component: NutritionNeedsPage,
    meta: { title: 'Nutrition Needs - LittleHelp', requiresAuth: true },
  },
  {
    path: '/child-info',
    name: 'ChildInfo',
    component: ChildInfoPage,
    meta: { title: 'Child Information - LittleHelp', requiresAuth: true },
  },
  {
    path: '/profile-summary',
    name: 'ProfileSummary',
    component: ProfileSummaryPage,
    meta: { title: 'Profile Summary - LittleHelp', requiresAuth: true },
  },
  {
    path: '/nutrition-check',
    name: 'NutritionCheck',
    component: NutritionCheckPage,
    meta: { title: 'Nutrition Check - LittleHelp', requiresAuth: true },
  },
  {
    path: '/nutrition-insights',
    name: 'NutritionInsights',
    component: NutritionInsightsPage,
    meta: { title: 'Nutrition Insights - LittleHelp', requiresAuth: true },
  },
  {
    path: '/weekly-plan',
    name: 'WeeklyPlan',
    component: WeeklyPlanPage,
    meta: { title: 'Weekly Plan - LittleHelp', requiresAuth: true },
  },
  {
    path: '/my-plans',
    name: 'MyPlans',
    component: MyPlansPage,
    meta: { title: 'My Plans - LittleHelp', requiresAuth: true },
  },
  {
    path: '/knowledge-hub-prototype',
    name: 'KnowledgeHubPrototype',
    component: KnowledgeHubPrototype,
    meta: { title: 'Knowledge Hub - LittleHelp' },
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
    if (to.hash) {
      return new Promise((resolve) => {
        setTimeout(() => {
          const el = document.querySelector(to.hash);
          if (el) {
            resolve({ el: to.hash, behavior: 'smooth', top: 24 });
          } else {
            resolve({ top: 0, behavior: 'smooth' });
          }
        }, 100);
      });
    }
    return { top: 0, behavior: 'smooth' };
  },
});

router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title || 'LittleHelp - Seasonal Lunchbox Planning';

  // 1. Project-wide access gate
  const projectAccess = localStorage.getItem('littlewell_project_access');

  if (!to.meta.skipProjectAccess && projectAccess !== 'granted') {
    return next({
      path: '/project-access',
      query: {
        redirect: to.fullPath,
      },
    });
  }

  // 2. User login gate for personal features
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