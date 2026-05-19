import { describe, it, expect, beforeEach, vi } from 'vitest';
import { createRouter, createMemoryHistory } from 'vue-router';
import { createPinia, setActivePinia } from 'pinia';

// We test the guard logic directly without importing the real router
// to avoid circular dependency with store imports

const mockAuthStore = {
  isAuthenticated: false,
};

vi.mock('@/stores/auth', () => ({
  useAuthStore: vi.fn(() => mockAuthStore),
}));

// Recreate the guard logic from router/index.js for isolated testing
function createTestRouter(isAuthenticated = false, projectAccess = 'granted') {
  mockAuthStore.isAuthenticated = isAuthenticated;

  const routes = [
    { path: '/', name: 'Home', component: { template: '<div />' }, meta: { title: 'Home' } },
    { path: '/login', name: 'Login', component: { template: '<div />' }, meta: { guestOnly: true } },
    { path: '/register', name: 'Register', component: { template: '<div />' }, meta: { guestOnly: true } },
    { path: '/child-info', name: 'ChildInfo', component: { template: '<div />' }, meta: { requiresAuth: true } },
    { path: '/weekly-plan', name: 'WeeklyPlan', component: { template: '<div />' }, meta: { requiresAuth: true } },
    { path: '/my-plans', name: 'MyPlans', component: { template: '<div />' }, meta: { requiresAuth: true } },
    { path: '/project-access', name: 'ProjectAccess', component: { template: '<div />' }, meta: { skipProjectAccess: true } },
    { path: '/quick-start', name: 'QuickStart', component: { template: '<div />' } },
  ];

  const router = createRouter({
    history: createMemoryHistory(),
    routes,
  });

  router.beforeEach(async (to, from, next) => {
    document.title = to.meta.title || 'LittleHelp';

    const access = projectAccess;
    if (!to.meta.skipProjectAccess && access !== 'granted') {
      return next({ path: '/project-access', query: { redirect: to.fullPath } });
    }

    if (to.meta.requiresAuth && !mockAuthStore.isAuthenticated) {
      return next({ path: '/login', query: { redirect: to.fullPath } });
    }

    if (to.meta.guestOnly && mockAuthStore.isAuthenticated) {
      return next('/');
    }

    next();
  });

  return router;
}

describe('Router guards', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('redirects to /project-access when project access is not granted', async () => {
    const router = createTestRouter(false, 'not-granted');
    await router.push('/');
    expect(router.currentRoute.value.path).toBe('/project-access');
  });

  it('allows navigation when project access is granted', async () => {
    const router = createTestRouter(false, 'granted');
    await router.push('/quick-start');
    expect(router.currentRoute.value.path).toBe('/quick-start');
  });

  it('redirects unauthenticated user to /login when accessing requiresAuth route', async () => {
    const router = createTestRouter(false, 'granted');
    await router.push('/child-info');
    expect(router.currentRoute.value.path).toBe('/login');
  });

  it('passes redirect query param when redirecting to login', async () => {
    const router = createTestRouter(false, 'granted');
    await router.push('/child-info');
    expect(router.currentRoute.value.query.redirect).toBe('/child-info');
  });

  it('allows authenticated user to access requiresAuth route', async () => {
    const router = createTestRouter(true, 'granted');
    await router.push('/child-info');
    expect(router.currentRoute.value.path).toBe('/child-info');
  });

  it('redirects authenticated user away from guestOnly route to home', async () => {
    const router = createTestRouter(true, 'granted');
    await router.push('/login');
    expect(router.currentRoute.value.path).toBe('/');
  });

  it('allows unauthenticated user to access guestOnly route', async () => {
    const router = createTestRouter(false, 'granted');
    await router.push('/login');
    expect(router.currentRoute.value.path).toBe('/login');
  });

  it('sets document title on navigation', async () => {
    const router = createTestRouter(false, 'granted');
    await router.push('/');
    expect(document.title).toBe('Home');
  });

  it('allows navigation to /project-access regardless of project access', async () => {
    const router = createTestRouter(false, 'not-granted');
    await router.push('/project-access');
    expect(router.currentRoute.value.path).toBe('/project-access');
  });
});
