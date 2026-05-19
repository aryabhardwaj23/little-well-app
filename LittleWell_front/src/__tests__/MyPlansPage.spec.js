import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';
import MyPlansPage from '@/views/MyPlansPage.vue';

// Mock API
vi.mock('@/services/api', () => ({
  getWeeklyPlans: vi.fn(() => Promise.resolve([])),
  deleteWeeklyPlan: vi.fn(() => Promise.resolve()),
  duplicateWeeklyPlan: vi.fn(() => Promise.resolve()),
}));

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: { template: '<div />' } },
    { path: '/my-plans', component: MyPlansPage },
    { path: '/weekly-plan', component: { template: '<div />' } },
    { path: '/results', component: { template: '<div />' } },
  ],
});

function mountPage() {
  return mount(MyPlansPage, {
    global: {
      plugins: [createPinia(), router],
      stubs: {
        ArrowLeft: true, BookmarkCheck: true, CalendarDays: true,
        UtensilsCrossed: true, Plus: true, Clock: true, ChefHat: true,
        Leaf: true, Eye: true, Edit: true, Copy: true, Trash2: true,
        Sparkles: true, Settings: true,
      },
    },
  });
}

describe('MyPlansPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
  });

  it('renders the page heading', () => {
    const wrapper = mountPage();
    expect(wrapper.text()).toContain('My Saved Plans');
  });

  it('renders two tab buttons', () => {
    const wrapper = mountPage();
    const tabs = wrapper.findAll('[role="tab"]');
    expect(tabs.length).toBe(2);
  });

  it('Weekly Plans tab is selected by default', () => {
    const wrapper = mountPage();
    const tabs = wrapper.findAll('[role="tab"]');
    const weeklyTab = tabs.find(t => t.text().includes('Weekly Plans'));
    expect(weeklyTab.attributes('aria-selected')).toBe('true');
  });

  it('Saved Lunchboxes tab is not selected by default', () => {
    const wrapper = mountPage();
    const tabs = wrapper.findAll('[role="tab"]');
    const lunchboxTab = tabs.find(t => t.text().includes('Saved Lunchboxes'));
    expect(lunchboxTab.attributes('aria-selected')).toBe('false');
  });

  it('clicking Saved Lunchboxes tab switches to that panel', async () => {
    const wrapper = mountPage();
    const tabs = wrapper.findAll('[role="tab"]');
    const lunchboxTab = tabs.find(t => t.text().includes('Saved Lunchboxes'));
    await lunchboxTab.trigger('click');
    expect(lunchboxTab.attributes('aria-selected')).toBe('true');
  });

  it('clicking Weekly Plans tab again switches back', async () => {
    const wrapper = mountPage();
    const tabs = wrapper.findAll('[role="tab"]');
    const lunchboxTab = tabs.find(t => t.text().includes('Saved Lunchboxes'));
    const weeklyTab = tabs.find(t => t.text().includes('Weekly Plans'));
    await lunchboxTab.trigger('click');
    await weeklyTab.trigger('click');
    expect(weeklyTab.attributes('aria-selected')).toBe('true');
  });

  it('weekly tab has correct aria-controls', () => {
    const wrapper = mountPage();
    const tabs = wrapper.findAll('[role="tab"]');
    const weeklyTab = tabs.find(t => t.text().includes('Weekly Plans'));
    expect(weeklyTab.attributes('aria-controls')).toBe('panel-weekly');
  });

  it('lunchboxes tab has correct aria-controls', () => {
    const wrapper = mountPage();
    const tabs = wrapper.findAll('[role="tab"]');
    const lunchboxTab = tabs.find(t => t.text().includes('Saved Lunchboxes'));
    expect(lunchboxTab.attributes('aria-controls')).toBe('panel-lunchboxes');
  });

  it('shows empty state when no weekly plans', async () => {
    const wrapper = mountPage();
    await new Promise(r => setTimeout(r, 50)); // wait for API mock
    expect(wrapper.text()).toContain('No weekly plans saved yet');
  });

  it('shows Create Weekly Plan button in empty state', async () => {
    const wrapper = mountPage();
    await new Promise(r => setTimeout(r, 50));
    const createBtn = wrapper.findAll('button').find(b => b.text().includes('Create Weekly Plan'));
    expect(createBtn).toBeTruthy();
  });
});
